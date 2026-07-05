import json
import os
from dataclasses import asdict
from typing import Any

from openai import AsyncOpenAI

from utils.models import (
    ExtractionResult,
    LLMVerificationConfig,
    LLMVerificationResult,
    QualityCheckResult,
)
from utils.text_utils import (
    navigation_noise_count,
    paragraph_count,
    repetition_ratio,
    text_preview,
)


TRUSTED_EXTRACTION_METHODS = {
    "hn_text",
    "pdfminer",
    "github_issue",
    "github_pull",
    "github_blob_raw",
    "github_readme",
    "trafilatura",
    "readability",
}


def run_basic_quality_check(
    story: dict[str, Any],
    extraction: ExtractionResult,
) -> QualityCheckResult:
    """Run a lightweight extraction-health check without judging article relevance."""
    text = extraction.text
    length = len(text)
    paragraphs = paragraph_count(text)
    repetition = repetition_ratio(text)
    noise_count = navigation_noise_count(text)

    reasons: list[str] = []
    score = 1.0

    if length == 0:
        score = 0.0
        reasons.append("no usable text extracted")
    else:
        reasons.append("text extracted")

    if noise_count <= 2:
        reasons.append("low navigation/cookie noise")
    else:
        score -= 0.3
        reasons.append("possible navigation/cookie noise detected")

    if repetition <= 0.92:
        reasons.append("text does not look severely repetitive")
    else:
        score -= 0.2
        reasons.append("text looks highly repetitive")

    if extraction.method in TRUSTED_EXTRACTION_METHODS:
        reasons.append("extraction method is a stronger source")
    elif extraction.method:
        score -= 0.1
        reasons.append("extraction method is a fallback source")
    else:
        score -= 0.3
        reasons.append("no extraction method produced content")

    score = max(0.0, min(score, 1.0))
    if length == 0:
        status = "failed"
    elif noise_count > 2 or repetition > 0.92 or extraction.method in {None, "meta_description"}:
        status = "partial"
    else:
        status = "success"

    return QualityCheckResult(
        status=status,
        passed=status in {"success", "partial"},
        score=round(score, 3),
        reasons=reasons,
        checks={
            "text_length": length,
            "paragraph_count": paragraphs,
            "repetition_ratio": round(repetition, 3),
            "navigation_noise_count": noise_count,
        },
    )


def should_use_web_search(
    config: LLMVerificationConfig,
    quality_check: QualityCheckResult,
) -> bool:
    """Decide whether LLM verification should use web search for this quality result."""
    if config.web_search_mode == "always":
        return True
    if config.web_search_mode == "off":
        return False
    return quality_check.status != "success"


def should_verify_with_llm(
    config: LLMVerificationConfig,
    quality_check: QualityCheckResult,
) -> bool:
    """Decide whether to run LLM verification manually or for extraction-health issues."""
    if config.enabled:
        return True
    if not config.auto_on_quality_issue:
        return False
    return quality_check.status in {"partial", "failed"}


def disabled_llm_result(reason: str) -> LLMVerificationResult:
    """Create a skipped LLM-verification result with the supplied reason."""
    return LLMVerificationResult(
        status="skipped",
        used_model=None,
        used_web_search=False,
        verdict=None,
        confidence=None,
        reasoning=None,
        problems=[],
        error=reason,
    )


def llm_verification_schema() -> dict[str, Any]:
    """Return the strict JSON schema expected from the LLM verification response."""
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "verdict": {
                "type": "string",
                "enum": ["pass", "partial", "fail"],
            },
            "confidence": {
                "type": "number",
                "minimum": 0,
                "maximum": 1,
            },
            "reasoning": {
                "type": "string",
            },
            "problems": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["verdict", "confidence", "reasoning", "problems"],
    }


def build_llm_verification_prompt(
    story: dict[str, Any],
    extraction: ExtractionResult,
    quality_check: QualityCheckResult,
    max_input_chars: int,
) -> str:
    """Build the prompt used to ask the LLM whether extracted content matches the HN story."""
    extracted_text = extraction.text[:max_input_chars]
    return f"""
Check whether the extracted content is the correct main content for this Hacker News story.

HN story title: {story.get("title")}
HN story URL: https://news.ycombinator.com/item?id={story.get("id")}
External URL: {story.get("url")}

Page title from fetched page: {extraction.page_title}
Meta description from fetched page: {extraction.meta_description}
Final fetched URL: {extraction.final_url}
Extraction method: {extraction.method}
Basic quality check: {json.dumps(asdict(quality_check), ensure_ascii=False)}

Extracted content preview:
{text_preview(extraction.text, 1200)}

Extracted content to judge:
{extracted_text}

Return JSON only. Mark:
- pass: content appears to be the article/post body for this story.
- partial: content is related but incomplete, noisy, or missing important body content.
- fail: content is unrelated, mostly navigation/login/cookie text, or not enough to verify.
""".strip()


async def verify_content_with_llm(
    story: dict[str, Any],
    extraction: ExtractionResult,
    quality_check: QualityCheckResult,
    config: LLMVerificationConfig,
) -> LLMVerificationResult:
    """Verify extracted content with OpenAI when configuration and quality status require it."""
    if not should_verify_with_llm(config, quality_check):
        return disabled_llm_result("LLM verification skipped because no verification trigger matched.")

    if not os.getenv("OPENAI_API_KEY"):
        return disabled_llm_result("OPENAI_API_KEY is not set.")

    use_web_search = should_use_web_search(config, quality_check)
    client = AsyncOpenAI()
    prompt = build_llm_verification_prompt(story, extraction, quality_check, config.max_input_chars)
    tools = [{"type": config.web_search_tool}] if use_web_search else []

    try:
        response = await client.responses.create(
            model=config.model,
            input=[
                {
                    "role": "developer",
                    "content": "You are a strict content extraction verifier. Judge only whether the extracted text matches the target HN story.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            tools=tools,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "content_extraction_verification",
                    "schema": llm_verification_schema(),
                    "strict": True,
                }
            },
        )
        data = json.loads(response.output_text)
        return LLMVerificationResult(
            status="completed",
            used_model=config.model,
            used_web_search=use_web_search,
            verdict=data.get("verdict"),
            confidence=data.get("confidence"),
            reasoning=data.get("reasoning"),
            problems=data.get("problems", []),
        )
    except Exception as exc:
        return LLMVerificationResult(
            status="error",
            used_model=config.model,
            used_web_search=use_web_search,
            verdict=None,
            confidence=None,
            reasoning=None,
            problems=[],
            error=str(exc),
        )
