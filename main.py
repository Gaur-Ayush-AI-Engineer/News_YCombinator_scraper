import asyncio
import logging
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import aiohttp
from dotenv import load_dotenv

from utils.comments import fetch_comments_for_story
from utils.extractors import extract_story_content
from utils.hn_api import fetch_top_stories
from utils.http_client import build_ssl_context
from utils.models import LLMVerificationConfig, SentimentAnalysisConfig, SummaryConfig
from utils.report_writer import write_outputs
from utils.sentiment import analyze_comment_sentiment
from utils.summarizer import summarize_story_content
from utils.text_utils import text_preview, truncate_text, unix_time_to_iso
from utils.content_checks import run_basic_quality_check, verify_content_with_llm


LOGGER = logging.getLogger(__name__)
PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")

OUTPUT_DIR = PROJECT_DIR / "outputs"
JSON_OUTPUT_PATH = OUTPUT_DIR / "raw_debug_output.json"
MARKDOWN_OUTPUT_PATH = OUTPUT_DIR / "raw_debug_output.md"
FINAL_JSON_OUTPUT_PATH = PROJECT_DIR / "final_report.json"
FINAL_MARKDOWN_OUTPUT_PATH = PROJECT_DIR / "final_report.md"


@dataclass
class PipelineConfig:
    """Runtime settings loaded from `.env` for one pipeline run."""

    story_limit: int
    max_comments_per_story: int
    reply_depth: int
    concurrency: int
    max_content_chars: int
    log_level: str


def env_bool(name: str, default: bool) -> bool:
    """Read a boolean setting from the environment."""
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() == "true"


def env_int(name: str, default: int) -> int:
    """Read an integer setting from the environment."""
    return int(os.getenv(name, str(default)))


def load_pipeline_config() -> PipelineConfig:
    """Load general pipeline settings from `.env`."""
    return PipelineConfig(
        story_limit=env_int("STORY_LIMIT", 10),
        max_comments_per_story=env_int("MAX_COMMENTS_PER_STORY", 100),
        reply_depth=env_int("REPLY_DEPTH", 2),
        concurrency=env_int("CONCURRENCY", 25),
        max_content_chars=env_int("MAX_CONTENT_CHARS", 25000),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )


def setup_logging(config: PipelineConfig) -> None:
    """Configure console logging for visible pipeline progress."""
    logging.basicConfig(
        level=getattr(logging, config.log_level, logging.INFO),
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def build_llm_config() -> LLMVerificationConfig:
    """Build the content-verification configuration from `.env`."""
    return LLMVerificationConfig(
        enabled=env_bool("LLM_VERIFY_ENABLED", False),
        auto_on_quality_issue=env_bool("AUTO_LLM_VERIFY_ON_QUALITY_ISSUE", True),
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        web_search_mode=os.getenv("LLM_WEB_SEARCH_MODE", "suspicious"),
        web_search_tool=os.getenv("LLM_WEB_SEARCH_TOOL", "web_search"),
        max_input_chars=env_int("LLM_MAX_INPUT_CHARS", 8000),
    )


def build_sentiment_config() -> SentimentAnalysisConfig:
    """Build the comment sentiment-analysis configuration from `.env`."""
    return SentimentAnalysisConfig(
        enabled=env_bool("SENTIMENT_ENABLED", True),
        model=os.getenv("SENTIMENT_MODEL", "gpt-5.4-nano"),
        top_n=env_int("SENTIMENT_TOP_N", 5),
        max_comments=env_int("SENTIMENT_MAX_COMMENTS", 100),
        max_comment_chars=env_int("SENTIMENT_MAX_COMMENT_CHARS", 1200),
    )


def build_summary_config() -> SummaryConfig:
    """Build the story summary-generation configuration from `.env`."""
    return SummaryConfig(
        enabled=env_bool("SUMMARY_ENABLED", True),
        model=os.getenv("SUMMARY_MODEL", "gpt-5.4-nano"),
        max_input_chars=env_int("SUMMARY_MAX_INPUT_CHARS", 12000),
    )


async def process_story(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    story: dict[str, Any],
    rank: int,
    max_comments: int,
    reply_depth: int,
    max_content_chars: int,
    llm_config: LLMVerificationConfig,
    sentiment_config: SentimentAnalysisConfig,
    summary_config: SummaryConfig,
) -> dict[str, Any]:
    """Fetch content, comments, quality checks, summary, and sentiment for one HN story."""
    LOGGER.info("Story %s: starting - %s", rank, story.get("title"))
    LOGGER.info("Story %s: extracting linked content and fetching comments", rank)
    extraction, comments = await asyncio.gather(
        extract_story_content(session, semaphore, story),
        fetch_comments_for_story(session, semaphore, story, max_comments, reply_depth),
    )
    LOGGER.info(
        "Story %s: extracted %s characters using %s; fetched %s comments",
        rank,
        len(extraction.text),
        extraction.method or "no extractor",
        len(comments),
    )

    quality_check = run_basic_quality_check(story, extraction)
    LOGGER.info(
        "Story %s: basic quality check is %s",
        rank,
        quality_check.status,
    )

    LOGGER.info("Story %s: running LLM verification, sentiment analysis, and summary steps", rank)
    llm_verification, sentiment_analysis, summary = await asyncio.gather(
        verify_content_with_llm(story, extraction, quality_check, llm_config),
        analyze_comment_sentiment(story, comments, sentiment_config),
        summarize_story_content(story, extraction.text, summary_config),
    )
    LOGGER.info(
        "Story %s: LLM verification=%s, sentiment=%s, summary=%s",
        rank,
        llm_verification.verdict or llm_verification.status,
        sentiment_analysis.status,
        summary.status,
    )
    content_text, content_truncated = truncate_text(extraction.text, max_content_chars)
    LOGGER.info("Story %s: completed", rank)

    return {
        "rank": rank,
        "story": {
            "id": story.get("id"),
            "title": story.get("title"),
            "hn_url": f"https://news.ycombinator.com/item?id={story.get('id')}",
            "external_url": story.get("url"),
            "by": story.get("by"),
            "score": story.get("score"),
            "descendants": story.get("descendants"),
            "time": unix_time_to_iso(story.get("time")),
            "type": story.get("type"),
        },
        "content": {
            "selected_method": extraction.method,
            "source_url": extraction.source_url,
            "final_url": extraction.final_url,
            "content_type": extraction.content_type,
            "url_type": extraction.url_type,
            "page_title": extraction.page_title,
            "meta_description": extraction.meta_description,
            "canonical_url": extraction.canonical_url,
            "text_length": len(extraction.text),
            "text_truncated": content_truncated,
            "text_preview": text_preview(extraction.text),
            "text": content_text,
            "extraction_attempts": [asdict(attempt) for attempt in extraction.attempts],
            "basic_quality_check": asdict(quality_check),
            "llm_verification": asdict(llm_verification),
            "summary": asdict(summary),
        },
        "comments": {
            "available_top_level_comment_count": len(story.get("kids", [])),
            "fetched_comment_count": len(comments),
            "max_comments": max_comments,
            "reply_depth": reply_depth,
            "items": comments,
            "sentiment_analysis": asdict(sentiment_analysis),
        },
    }


async def run_pipeline(config: PipelineConfig) -> dict[str, Any]:
    """Run the full async pipeline and return the complete structured output."""
    LOGGER.info("Creating output directory: %s", OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    semaphore = asyncio.Semaphore(config.concurrency)
    connector = aiohttp.TCPConnector(ssl=build_ssl_context(), limit=config.concurrency)
    llm_config = build_llm_config()
    sentiment_config = build_sentiment_config()
    summary_config = build_summary_config()
    LOGGER.info(
        "Config: stories=%s, max_comments=%s, reply_depth=%s, summary=%s, sentiment=%s",
        config.story_limit,
        config.max_comments_per_story,
        config.reply_depth,
        summary_config.enabled,
        sentiment_config.enabled,
    )

    async with aiohttp.ClientSession(connector=connector) as session:
        LOGGER.info("Fetching top %s Hacker News stories", config.story_limit)
        stories = await fetch_top_stories(session, semaphore, config.story_limit)
        LOGGER.info("Fetched %s stories; processing with concurrency=%s", len(stories), config.concurrency)
        processed = await asyncio.gather(
            *(
                process_story(
                    session=session,
                    semaphore=semaphore,
                    story=story,
                    rank=rank,
                    max_comments=config.max_comments_per_story,
                    reply_depth=config.reply_depth,
                    max_content_chars=config.max_content_chars,
                    llm_config=llm_config,
                    sentiment_config=sentiment_config,
                    summary_config=summary_config,
                )
                for rank, story in enumerate(stories, start=1)
            )
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "config": {
            "story_limit": config.story_limit,
            "max_comments_per_story": config.max_comments_per_story,
            "reply_depth": config.reply_depth,
            "concurrency": config.concurrency,
            "max_content_chars": config.max_content_chars,
            "llm_verification": asdict(llm_config),
            "sentiment_analysis": asdict(sentiment_config),
            "summary": asdict(summary_config),
        },
        "stories": processed,
    }


def count_step_status(output: dict[str, Any], section: str, step: str, status: str) -> int:
    """Count stories where a nested pipeline step has the requested status."""
    return sum(
        1
        for item in output["stories"]
        if item[section][step]["status"] == status
    )


def print_completion_summary(output: dict[str, Any]) -> None:
    """Print a short run summary after reports are written."""
    successes = count_step_status(output, "content", "basic_quality_check", "success")
    partials = count_step_status(output, "content", "basic_quality_check", "partial")
    failures = count_step_status(output, "content", "basic_quality_check", "failed")
    llm_completed = count_step_status(output, "content", "llm_verification", "completed")
    sentiment_completed = count_step_status(output, "comments", "sentiment_analysis", "completed")
    summaries_completed = count_step_status(output, "content", "summary", "completed")

    print("Hacker News top stories pipeline completed")
    print(f"Stories processed: {len(output['stories'])}")
    print(f"Basic quality check: {successes} success, {partials} partial, {failures} failed")
    print(f"LLM verifications completed: {llm_completed}")
    print(f"Sentiment analyses completed: {sentiment_completed}")
    print(f"Summaries completed: {summaries_completed}")
    print(f"JSON output: {JSON_OUTPUT_PATH}")
    print(f"Markdown report: {MARKDOWN_OUTPUT_PATH}")
    print(f"Final JSON output: {FINAL_JSON_OUTPUT_PATH}")
    print(f"Final Markdown report: {FINAL_MARKDOWN_OUTPUT_PATH}")


def main() -> None:
    """Run the CLI entry point, write reports, and print a short completion summary."""
    config = load_pipeline_config()
    setup_logging(config)
    LOGGER.info("Starting Hacker News top stories pipeline")
    output = asyncio.run(run_pipeline(config))
    LOGGER.info("Writing JSON and Markdown reports")
    write_outputs(
        output,
        JSON_OUTPUT_PATH,
        MARKDOWN_OUTPUT_PATH,
        FINAL_JSON_OUTPUT_PATH,
        FINAL_MARKDOWN_OUTPUT_PATH,
    )
    LOGGER.info("Reports written successfully")
    print_completion_summary(output)


if __name__ == "__main__":
    main()
