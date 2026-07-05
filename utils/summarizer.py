import json
import os
from typing import Any

from openai import AsyncOpenAI

from utils.models import SummaryConfig, SummaryResult
from utils.text_utils import text_preview


def skipped_summary(reason: str) -> SummaryResult:
    """Create a skipped summary result with a clear reason."""
    return SummaryResult(
        status="skipped",
        used_model=None,
        summary=None,
        error=reason,
    )


def summary_schema() -> dict[str, Any]:
    """Return the strict JSON schema expected from the summary response."""
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "summary": {"type": "string"},
        },
        "required": ["summary"],
    }


def build_summary_prompt(
    story: dict[str, Any],
    extracted_text: str,
    max_input_chars: int,
) -> str:
    """Build the prompt used to summarize extracted story content."""
    return f"""
Summarize this Hacker News story's linked content.

Story title: {story.get("title")}
HN URL: https://news.ycombinator.com/item?id={story.get("id")}
External URL: {story.get("url")}

Write a concise 3-5 sentence summary. Focus on the article/post content, not the Hacker News discussion.

Content preview:
{text_preview(extracted_text, 1000)}

Content:
{extracted_text[:max_input_chars]}
""".strip()


async def summarize_story_content(
    story: dict[str, Any],
    extracted_text: str,
    config: SummaryConfig,
) -> SummaryResult:
    """Generate a concise story summary with OpenAI when summary generation is enabled."""
    if not config.enabled:
        return skipped_summary("Summary generation is disabled.")

    if not os.getenv("OPENAI_API_KEY"):
        return skipped_summary("OPENAI_API_KEY is not set.")

    if not extracted_text.strip():
        return SummaryResult(
            status="completed",
            used_model=config.model,
            summary="No article content was extracted for this story.",
        )

    client = AsyncOpenAI()
    prompt = build_summary_prompt(story, extracted_text, config.max_input_chars)

    try:
        response = await client.responses.create(
            model=config.model,
            input=[
                {
                    "role": "developer",
                    "content": "You write concise, faithful summaries of extracted article content. Return only schema-valid JSON.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "story_summary",
                    "schema": summary_schema(),
                    "strict": True,
                }
            },
        )
        data = json.loads(response.output_text)
        return SummaryResult(
            status="completed",
            used_model=config.model,
            summary=data.get("summary"),
        )
    except Exception as exc:
        return SummaryResult(
            status="error",
            used_model=config.model,
            summary=None,
            error=str(exc),
        )
