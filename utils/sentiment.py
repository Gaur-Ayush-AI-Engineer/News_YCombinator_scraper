import json
import os
from typing import Any

from openai import AsyncOpenAI

from utils.models import SentimentAnalysisConfig, SentimentAnalysisResult


def disabled_sentiment_result(reason: str) -> SentimentAnalysisResult:
    """Create a skipped sentiment-analysis result with the supplied reason."""
    return SentimentAnalysisResult(
        status="skipped",
        used_model=None,
        analyzed_comment_count=0,
        top_positive=[],
        top_negative=[],
        error=reason,
    )


def sentiment_schema() -> dict[str, Any]:
    """Return the strict JSON schema expected from the sentiment-analysis response."""
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "comment_id": {"type": "integer"},
                        "sentiment": {
                            "type": "string",
                            "enum": ["positive", "negative", "neutral", "mixed"],
                        },
                        "sentiment_score": {
                            "type": "number",
                            "minimum": -1,
                            "maximum": 1,
                        },
                        "confidence": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 1,
                        },
                        "reason": {"type": "string"},
                    },
                    "required": [
                        "comment_id",
                        "sentiment",
                        "sentiment_score",
                        "confidence",
                        "reason",
                    ],
                },
            }
        },
        "required": ["items"],
    }


def prepare_comments(
    comments: list[dict[str, Any]],
    max_comments: int,
    max_comment_chars: int,
) -> list[dict[str, Any]]:
    """Select non-empty comments and trim each comment before sending it to the LLM."""
    prepared = []
    for comment in comments:
        text = (comment.get("text") or "").strip()
        if not text:
            continue

        prepared.append(
            {
                "id": comment.get("id"),
                "by": comment.get("by"),
                "depth": comment.get("depth"),
                "text": text[:max_comment_chars],
            }
        )

        if len(prepared) >= max_comments:
            break

    return prepared


def build_sentiment_prompt(
    story: dict[str, Any],
    comments: list[dict[str, Any]],
) -> str:
    """Build the prompt used to classify comment sentiment for one story."""
    return f"""
Analyze Hacker News comments for sentiment toward this story/topic.

Story title: {story.get("title")}
Story URL: https://news.ycombinator.com/item?id={story.get("id")}
External URL: {story.get("url")}

For each comment, assign:
- sentiment: positive, negative, neutral, or mixed
- sentiment_score: -1.0 very negative, 0 neutral/mixed, +1.0 very positive
- confidence: how confident you are
- reason: short explanation

Important:
- Judge the commenter's attitude toward the story/topic, not random emotional words.
- Technical disagreement, criticism, risk concerns, or distrust should usually be negative.
- Praise, agreement, excitement, usefulness, or support should usually be positive.
- Sarcasm should be interpreted by meaning, not surface words.
- Keep neutral or mixed comments near 0.

Comments JSON:
{json.dumps(comments, ensure_ascii=False)}
""".strip()


def attach_comment_text(
    scored_items: list[dict[str, Any]],
    comments_by_id: dict[int, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Attach original comment metadata and text to LLM sentiment scores."""
    enriched = []
    for item in scored_items:
        comment_id = item.get("comment_id")
        original = comments_by_id.get(comment_id, {})
        enriched.append(
            {
                "comment_id": comment_id,
                "by": original.get("by"),
                "depth": original.get("depth"),
                "text": original.get("text"),
                "sentiment": item.get("sentiment"),
                "sentiment_score": item.get("sentiment_score"),
                "confidence": item.get("confidence"),
                "reason": item.get("reason"),
            }
        )
    return enriched


async def analyze_comment_sentiment(
    story: dict[str, Any],
    comments: list[dict[str, Any]],
    config: SentimentAnalysisConfig,
) -> SentimentAnalysisResult:
    """Analyze comments with OpenAI and return the top positive and negative comments."""
    if not config.enabled:
        return disabled_sentiment_result("Sentiment analysis is disabled.")

    if not os.getenv("OPENAI_API_KEY"):
        return disabled_sentiment_result("OPENAI_API_KEY is not set.")

    prepared_comments = prepare_comments(comments, config.max_comments, config.max_comment_chars)
    if not prepared_comments:
        return SentimentAnalysisResult(
            status="completed",
            used_model=config.model,
            analyzed_comment_count=0,
            top_positive=[],
            top_negative=[],
        )

    comments_by_id = {comment["id"]: comment for comment in prepared_comments}
    client = AsyncOpenAI()
    prompt = build_sentiment_prompt(story, prepared_comments)

    try:
        response = await client.responses.create(
            model=config.model,
            input=[
                {
                    "role": "developer",
                    "content": "You are a careful sentiment analyst for technical discussion comments. Return only schema-valid JSON.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "hn_comment_sentiment",
                    "schema": sentiment_schema(),
                    "strict": True,
                }
            },
        )
        data = json.loads(response.output_text)
        scored_items = data.get("items", [])
        positive = sorted(
            (item for item in scored_items if item.get("sentiment_score", 0) > 0),
            key=lambda item: (item.get("sentiment_score", 0), item.get("confidence", 0)),
            reverse=True,
        )[: config.top_n]
        negative = sorted(
            (item for item in scored_items if item.get("sentiment_score", 0) < 0),
            key=lambda item: (item.get("sentiment_score", 0), -item.get("confidence", 0)),
        )[: config.top_n]

        return SentimentAnalysisResult(
            status="completed",
            used_model=config.model,
            analyzed_comment_count=len(prepared_comments),
            top_positive=attach_comment_text(positive, comments_by_id),
            top_negative=attach_comment_text(negative, comments_by_id),
        )
    except Exception as exc:
        return SentimentAnalysisResult(
            status="error",
            used_model=config.model,
            analyzed_comment_count=len(prepared_comments),
            top_positive=[],
            top_negative=[],
            error=str(exc),
        )
