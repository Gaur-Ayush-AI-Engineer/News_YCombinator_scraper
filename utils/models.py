from dataclasses import dataclass
from typing import Any


@dataclass
class FetchResult:
    body: bytes
    content_type: str
    final_url: str


@dataclass
class ExtractionAttempt:
    method: str
    ok: bool
    text_length: int = 0
    error: str | None = None


@dataclass
class ExtractionResult:
    method: str | None
    text: str
    source_url: str | None
    final_url: str | None
    content_type: str | None
    url_type: str
    page_title: str | None
    meta_description: str | None
    canonical_url: str | None
    attempts: list[ExtractionAttempt]


@dataclass
class GitHubExtractionResult:
    method: str
    text: str
    content_type: str
    page_title: str | None = None
    meta_description: str | None = None


@dataclass
class QualityCheckResult:
    status: str
    passed: bool
    score: float
    reasons: list[str]
    checks: dict[str, Any]


@dataclass
class LLMVerificationConfig:
    enabled: bool
    auto_on_quality_issue: bool
    model: str
    web_search_mode: str
    web_search_tool: str
    max_input_chars: int


@dataclass
class LLMVerificationResult:
    status: str
    used_model: str | None
    used_web_search: bool
    verdict: str | None
    confidence: float | None
    reasoning: str | None
    problems: list[str]
    error: str | None = None


@dataclass
class SentimentAnalysisConfig:
    enabled: bool
    model: str
    top_n: int
    max_comments: int
    max_comment_chars: int


@dataclass
class SentimentAnalysisResult:
    status: str
    used_model: str | None
    analyzed_comment_count: int
    top_positive: list[dict[str, Any]]
    top_negative: list[dict[str, Any]]
    error: str | None = None


@dataclass
class SummaryConfig:
    enabled: bool
    model: str
    max_input_chars: int


@dataclass
class SummaryResult:
    status: str
    used_model: str | None
    summary: str | None
    error: str | None = None
