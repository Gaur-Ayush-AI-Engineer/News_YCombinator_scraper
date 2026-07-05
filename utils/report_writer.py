import json
import re
from pathlib import Path
from typing import Any


def short_comment(value: str | None, limit: int = 260) -> str:
    """Clean and shorten a comment for markdown display."""
    value = " ".join((value or "").split())
    if len(value) <= limit:
        return value
    return value[:limit].rstrip() + "..."


def add_sentiment_comments(
    lines: list[str],
    heading: str,
    comments: list[dict[str, Any]],
) -> None:
    """Append a sentiment-comment section to a markdown line list."""
    lines.extend([f"#### {heading}", ""])
    if not comments:
        lines.extend(["_No comments selected._", ""])
        return

    for comment in comments:
        score = comment.get("sentiment_score")
        confidence = comment.get("confidence")
        lines.extend(
            [
                f"- `{comment.get('comment_id')}` by `{comment.get('by')}` "
                f"(score: {score}, confidence: {confidence})",
                f"  {short_comment(comment.get('text'))}",
                "",
            ]
        )


def build_markdown_report(output: dict[str, Any]) -> str:
    """Build the full markdown report with extraction details and content previews."""
    lines = [
        "# Hacker News Top Stories",
        "",
        f"Generated at: `{output['generated_at']}`",
        "",
        "| Rank | Story | Score | Quality Check | LLM Verification | Sentiment | Comments | Method |",
        "| --- | --- | ---: | --- | --- | --- | ---: | --- |",
    ]

    for item in output["stories"]:
        story = item["story"]
        content = item["content"]
        quality_check = content["basic_quality_check"]
        llm_verification = content.get("llm_verification", {})
        sentiment = item["comments"].get("sentiment_analysis", {})
        llm_label = llm_verification.get("verdict") or llm_verification.get("status") or "off"
        sentiment_label = sentiment.get("status") or "off"
        title = (story.get("title") or "").replace("|", "\\|")
        hn_url = story.get("hn_url")
        method = content.get("selected_method") or "none"
        lines.append(
            f"| {item['rank']} | [{title}]({hn_url}) | {story.get('score') or 0} | "
            f"{quality_check['status']} ({content['text_length']} chars) | "
            f"{llm_label} | {sentiment_label} | {item['comments']['fetched_comment_count']} | {method} |"
        )

    lines.extend(["", "## Content Previews", ""])
    for item in output["stories"]:
        story = item["story"]
        content = item["content"]
        llm_verification = content.get("llm_verification", {})
        sentiment = item["comments"].get("sentiment_analysis", {})
        lines.extend(
            [
                f"### {item['rank']}. {story.get('title')}",
                "",
                f"- HN: {story.get('hn_url')}",
                f"- External: {story.get('external_url') or 'N/A'}",
                f"- Extraction: {content.get('selected_method') or 'none'}",
                f"- Basic quality check: {content['basic_quality_check']['status']}, score {content['basic_quality_check']['score']}",
                f"- LLM verification: {llm_verification.get('verdict') or llm_verification.get('status') or 'off'}",
                f"- Sentiment analysis: {sentiment.get('status') or 'off'}",
                f"- Comments fetched: {item['comments']['fetched_comment_count']}",
                "",
                content.get("text_preview") or "_No content extracted._",
                "",
            ]
        )
        if sentiment.get("status") == "completed":
            add_sentiment_comments(lines, "Top Positive Comments", sentiment.get("top_positive", []))
            add_sentiment_comments(lines, "Top Negative Comments", sentiment.get("top_negative", []))

    return "\n".join(lines)


def build_final_output(output: dict[str, Any]) -> dict[str, Any]:
    """Build the clean deliverable JSON with summary and selected comments only."""
    stories = []
    for item in output["stories"]:
        story = item["story"]
        content = item["content"]
        sentiment = item["comments"].get("sentiment_analysis", {})
        summary = content.get("summary", {})
        quality_check = content.get("basic_quality_check", {})
        llm_verification = content.get("llm_verification", {})
        story_output = {
            "serial_number": item["rank"],
            "heading": story.get("title"),
            "hn_url": story.get("hn_url"),
            "external_url": story.get("external_url"),
            "summary": summary.get("summary"),
            "top_positive_comments": final_comment_texts(sentiment.get("top_positive", [])),
            "top_negative_comments": final_comment_texts(sentiment.get("top_negative", [])),
        }

        extraction_note = final_extraction_note(quality_check, llm_verification)
        if extraction_note:
            story_output["extraction_note"] = extraction_note

        stories.append(story_output)

    return {"stories": stories}


def final_extraction_note(
    quality_check: dict[str, Any],
    llm_verification: dict[str, Any],
) -> str | None:
    """Return an extraction note only when the final output needs an issue explanation."""
    llm_status = llm_verification.get("status")
    llm_verdict = llm_verification.get("verdict")

    if llm_status == "completed" and llm_verdict == "pass":
        return None
    if llm_status == "completed" and llm_verdict in {"partial", "fail"}:
        return llm_verification.get("reasoning")
    if quality_check.get("status") in {"partial", "failed"}:
        return llm_verification.get("reasoning") or "; ".join(
            quality_check.get("reasons", [])
        )
    return None


def final_comment_texts(comments: list[dict[str, Any]]) -> list[str]:
    """Return only the selected comment texts for the final deliverable JSON."""
    return [clean_final_comment_text(comment.get("text")) for comment in comments]


def clean_final_comment_text(value: str | None) -> str:
    """Remove HN quote markers from final comment text."""
    value = " ".join((value or "").split())
    value = re.sub(r"(^|\s)>+\s*", " ", value)
    return " ".join(value.split())


def add_final_comment_block(
    lines: list[str],
    heading: str,
    comments: list[str],
) -> None:
    """Append a final-report comment list to a markdown line list."""
    lines.extend([f"#### {heading}", ""])
    if not comments:
        lines.extend(["_No comments available._", ""])
        return

    for index, comment in enumerate(comments, start=1):
        lines.extend([f"{index}. {short_comment(comment, 420)}", ""])


def build_final_markdown_report(output: dict[str, Any]) -> str:
    """Build the clean markdown deliverable for story summaries and top comments."""
    final_output = build_final_output(output)
    lines = ["# Hacker News Final Output", ""]

    for story in final_output["stories"]:
        lines.extend(
            [
                f"## {story['serial_number']}. {story.get('heading')}",
                "",
                f"- HN: {story.get('hn_url')}",
                f"- External: {story.get('external_url') or 'N/A'}",
                "",
                "### Summary",
                "",
                story.get("summary") or "_Summary not generated. Run with `--final-output` or `--summarize` after setting `OPENAI_API_KEY`._",
                "",
            ]
        )
        if story.get("extraction_note"):
            lines.extend(
                [
                    "### Extraction Note",
                    "",
                    story["extraction_note"],
                    "",
                ]
            )
        add_final_comment_block(lines, "Top 5 Positive Comments", story.get("top_positive_comments", []))
        add_final_comment_block(lines, "Top 5 Negative Comments", story.get("top_negative_comments", []))

    return "\n".join(lines)


def write_outputs(
    output: dict[str, Any],
    json_output_path: Path,
    markdown_output_path: Path,
    final_json_output_path: Path,
    final_markdown_output_path: Path,
) -> None:
    """Write the full and final JSON/markdown outputs to disk."""
    json_output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    markdown_output_path.write_text(build_markdown_report(output), encoding="utf-8")
    final_json_output_path.write_text(
        json.dumps(build_final_output(output), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    final_markdown_output_path.write_text(build_final_markdown_report(output), encoding="utf-8")
