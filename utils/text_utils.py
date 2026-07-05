import re
from datetime import datetime, timezone
from difflib import SequenceMatcher
from html import unescape


def clean_html_text(value: str | None) -> str:
    """Remove simple HTML markup, decode entities, and normalize whitespace."""
    if not value:
        return ""

    value = re.sub(r"<br\s*/?>", "\n", value, flags=re.IGNORECASE)
    value = re.sub(r"</p\s*>", "\n\n", value, flags=re.IGNORECASE)
    value = re.sub(r"</li\s*>", "\n", value, flags=re.IGNORECASE)
    value = re.sub(r"<[^>]+>", " ", value)
    value = unescape(value)
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def normalize_text(value: str | None) -> str:
    """Clean text and collapse all whitespace into single spaces."""
    value = clean_html_text(value)
    return re.sub(r"\s+", " ", value).strip()


def normalize_for_match(value: str | None) -> str:
    """Normalize text for loose matching by lowercasing and removing punctuation."""
    value = normalize_text(value).lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def text_preview(value: str, limit: int = 900) -> str:
    """Return a cleaned preview string capped at the requested character limit."""
    value = normalize_text(value)
    if len(value) <= limit:
        return value
    return value[:limit].rstrip() + "..."


def truncate_text(value: str, limit: int) -> tuple[str, bool]:
    """Return text capped to a limit plus a flag showing whether truncation happened."""
    if len(value) <= limit:
        return value, False
    return value[:limit].rstrip() + "\n\n[TRUNCATED]", True


def unix_time_to_iso(value: int | None) -> str | None:
    """Convert a Unix timestamp to an ISO-8601 UTC string."""
    if value is None:
        return None
    return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()


def similarity(left: str | None, right: str | None) -> float:
    """Return a loose 0-to-1 similarity score between two text values."""
    left = normalize_for_match(left)
    right = normalize_for_match(right)
    if not left or not right:
        return 0.0
    return SequenceMatcher(None, left, right).ratio()


def compact_contains_title(title: str | None, text: str) -> bool:
    """Check whether a normalized story title appears inside normalized text."""
    title = normalize_for_match(title)
    text = normalize_for_match(text)
    if not title or not text:
        return False
    return title in text


def paragraph_count(text: str) -> int:
    """Estimate the number of paragraph-like sections in text for debugging output."""
    paragraphs = re.split(r"\n{2,}|(?<=[.!?])\s+(?=[A-Z0-9])", text)
    return len([paragraph for paragraph in paragraphs if len(paragraph.strip()) >= 80])


def repetition_ratio(text: str) -> float:
    """Estimate repeated-word density; higher values mean more repeated words."""
    words = re.findall(r"[a-zA-Z0-9]{3,}", text.lower())
    if not words:
        return 1.0
    return 1.0 - (len(set(words)) / len(words))


def navigation_noise_count(text: str) -> int:
    """Count common navigation, login, subscription, and cookie-banner markers."""
    lowered = text.lower()
    noise_markers = [
        "cookie policy",
        "privacy policy",
        "terms of service",
        "sign in",
        "sign up",
        "subscribe",
        "accept cookies",
        "enable javascript",
    ]
    return sum(lowered.count(marker) for marker in noise_markers)
