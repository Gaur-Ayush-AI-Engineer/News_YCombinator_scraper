import asyncio
from io import BytesIO
from typing import Any
from urllib.parse import urlparse

import aiohttp
import trafilatura
from lxml import html as lxml_html
from pdfminer.high_level import extract_text as extract_pdf_text
from readability import Document as ReadabilityDocument

from utils.http_client import fetch_bytes, fetch_json
from utils.models import ExtractionAttempt, ExtractionResult, GitHubExtractionResult
from utils.text_utils import clean_html_text, normalize_text


def detect_url_type(url: str | None, content_type: str | None = None) -> str:
    """Classify a story URL as HN text, PDF, GitHub, HTML, or other content."""
    if not url:
        return "hn_text"

    parsed = urlparse(url)
    path = parsed.path.lower()
    netloc = parsed.netloc.lower()
    content_type = (content_type or "").lower()

    if "pdf" in content_type or path.endswith(".pdf"):
        return "pdf"
    if netloc in {"github.com", "www.github.com"}:
        return "github"
    if "text/html" in content_type or not content_type:
        return "html"
    return "other"


def try_hn_text(story: dict[str, Any], attempts: list[ExtractionAttempt]) -> str:
    """Extract inline text from an HN story item and record the attempt."""
    text = clean_html_text(story.get("text"))
    attempts.append(
        ExtractionAttempt(
            method="hn_text",
            ok=bool(text),
            text_length=len(text),
            error=None if text else "Story does not contain inline HN text.",
        )
    )
    return text


def extract_html_metadata(html_text: str) -> dict[str, str | None]:
    """Extract page title, meta description, and canonical URL from HTML."""
    try:
        document = lxml_html.fromstring(html_text)
        title_values = document.xpath("//title/text()")
        description_values = document.xpath(
            "//meta[translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='description']/@content"
            " | //meta[translate(@property, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='og:description']/@content"
        )
        canonical_values = document.xpath("//link[translate(@rel, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='canonical']/@href")
        return {
            "page_title": normalize_text(title_values[0]) if title_values else None,
            "meta_description": normalize_text(description_values[0]) if description_values else None,
            "canonical_url": canonical_values[0] if canonical_values else None,
        }
    except Exception:
        return {
            "page_title": None,
            "meta_description": None,
            "canonical_url": None,
        }


def try_pdf_extraction(
    body: bytes,
    content_type: str,
    story_url: str,
    attempts: list[ExtractionAttempt],
) -> str:
    """Extract text from a PDF response when the URL or content type looks like a PDF."""
    if detect_url_type(story_url, content_type) != "pdf":
        attempts.append(
            ExtractionAttempt(
                method="pdfminer",
                ok=False,
                error="URL/content-type does not look like a PDF.",
            )
        )
        return ""

    try:
        text = normalize_text(extract_pdf_text(BytesIO(body)))
        attempts.append(ExtractionAttempt(method="pdfminer", ok=bool(text), text_length=len(text)))
        return text
    except Exception as exc:
        attempts.append(ExtractionAttempt(method="pdfminer", ok=False, error=str(exc)))
        return ""


async def try_github_content(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    story_url: str,
    attempts: list[ExtractionAttempt],
) -> GitHubExtractionResult | None:
    """Extract useful text from GitHub issues, pull requests, blobs, or README files."""
    parsed = urlparse(story_url)
    if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
        attempts.append(ExtractionAttempt(method="github", ok=False, error="URL is not a GitHub URL."))
        return None

    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        attempts.append(
            ExtractionAttempt(
                method="github",
                ok=False,
                error="GitHub URL does not include owner/repo path.",
            )
        )
        return None

    owner, repo = parts[0], parts[1]

    if len(parts) >= 4 and parts[2] == "issues" and parts[3].isdigit():
        issue_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{parts[3]}"
        try:
            issue = await fetch_json(session, semaphore, issue_url)
            title = issue.get("title", "")
            body = issue.get("body") or ""
            text = normalize_text(f"{title}\n\n{body}")
            if text:
                attempts.append(ExtractionAttempt(method="github_issue", ok=True, text_length=len(text)))
                return GitHubExtractionResult(
                    method="github_issue",
                    text=text,
                    content_type="application/json",
                    page_title=normalize_text(title),
                    meta_description=normalize_text(body[:300]),
                )
        except Exception as exc:
            attempts.append(ExtractionAttempt(method="github_issue", ok=False, error=str(exc)))

    if len(parts) >= 4 and parts[2] == "pull" and parts[3].isdigit():
        pull_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{parts[3]}"
        try:
            pull = await fetch_json(session, semaphore, pull_url)
            title = pull.get("title", "")
            body = pull.get("body") or ""
            text = normalize_text(f"{title}\n\n{body}")
            if text:
                attempts.append(ExtractionAttempt(method="github_pull", ok=True, text_length=len(text)))
                return GitHubExtractionResult(
                    method="github_pull",
                    text=text,
                    content_type="application/json",
                    page_title=normalize_text(title),
                    meta_description=normalize_text(body[:300]),
                )
        except Exception as exc:
            attempts.append(ExtractionAttempt(method="github_pull", ok=False, error=str(exc)))

    if len(parts) >= 5 and parts[2] == "blob":
        branch = parts[3]
        file_path = "/".join(parts[4:])
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file_path}"
        try:
            result = await fetch_bytes(session, semaphore, raw_url)
            text = normalize_text(result.body.decode("utf-8", errors="replace"))
            if text:
                attempts.append(ExtractionAttempt(method="github_blob_raw", ok=True, text_length=len(text)))
                return GitHubExtractionResult(
                    method="github_blob_raw",
                    text=text,
                    content_type=result.content_type or "text/plain",
                    page_title=file_path,
                    meta_description=text[:300],
                )
        except Exception as exc:
            attempts.append(ExtractionAttempt(method="github_blob_raw", ok=False, error=str(exc)))

    readme_urls = [
        f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/README.md",
        f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md",
        f"https://raw.githubusercontent.com/{owner}/{repo}/master/README.md",
    ]

    for readme_url in readme_urls:
        try:
            result = await fetch_bytes(session, semaphore, readme_url)
        except Exception:
            continue

        text = normalize_text(result.body.decode("utf-8", errors="replace"))
        if text:
            attempts.append(ExtractionAttempt(method="github_readme", ok=True, text_length=len(text)))
            return GitHubExtractionResult(
                method="github_readme",
                text=text,
                content_type=result.content_type or "text/markdown",
                page_title=f"{owner}/{repo} README",
                meta_description=text[:300],
            )

    attempts.append(ExtractionAttempt(method="github_readme", ok=False, error="GitHub content was not found."))
    return None


def try_trafilatura(
    html_text: str,
    story_url: str,
    attempts: list[ExtractionAttempt],
) -> str:
    """Extract article-like text from HTML using trafilatura."""
    try:
        text = normalize_text(
            trafilatura.extract(
                html_text,
                url=story_url,
                include_comments=False,
                include_tables=False,
            )
        )
        attempts.append(ExtractionAttempt(method="trafilatura", ok=bool(text), text_length=len(text)))
        return text
    except Exception as exc:
        attempts.append(ExtractionAttempt(method="trafilatura", ok=False, error=str(exc)))
        return ""


def try_readability(html_text: str, attempts: list[ExtractionAttempt]) -> str:
    """Extract article-like text from HTML using readability-lxml."""
    try:
        doc = ReadabilityDocument(html_text)
        text = clean_html_text(doc.summary())
        attempts.append(ExtractionAttempt(method="readability", ok=bool(text), text_length=len(text)))
        return text
    except Exception as exc:
        attempts.append(ExtractionAttempt(method="readability", ok=False, error=str(exc)))
        return ""


def try_lxml_main_content(html_text: str, attempts: list[ExtractionAttempt]) -> str:
    """Extract text from article/main/body candidates using lxml as a fallback."""
    try:
        document = lxml_html.fromstring(html_text)
        for element in document.xpath(
            "//script|//style|//noscript|//svg|//form|//nav|//header|//footer|//aside"
        ):
            element.drop_tree()

        candidates = document.xpath("//article|//main|//*[@role='main']")
        if not candidates:
            body = document.find("body")
            candidates = [body if body is not None else document]

        candidate_texts = [normalize_text(" ".join(candidate.itertext())) for candidate in candidates]
        text = max(candidate_texts, key=len, default="")
        attempts.append(ExtractionAttempt(method="lxml_main_content", ok=bool(text), text_length=len(text)))
        return text
    except Exception as exc:
        attempts.append(ExtractionAttempt(method="lxml_main_content", ok=False, error=str(exc)))
        return ""


def try_meta_description(
    metadata: dict[str, str | None],
    attempts: list[ExtractionAttempt],
) -> str:
    """Use the page meta description as a final small-content fallback."""
    text = normalize_text(metadata.get("meta_description"))
    attempts.append(ExtractionAttempt(method="meta_description", ok=bool(text), text_length=len(text)))
    return text


async def extract_story_content(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    story: dict[str, Any],
) -> ExtractionResult:
    """Run all content-extraction fallbacks for one HN story and return the best result."""
    attempts: list[ExtractionAttempt] = []
    story_url = story.get("url")

    hn_text = try_hn_text(story, attempts)
    if hn_text and not story_url:
        return ExtractionResult(
            method="hn_text",
            text=hn_text,
            source_url=None,
            final_url=None,
            content_type=None,
            url_type="hn_text",
            page_title=story.get("title"),
            meta_description=None,
            canonical_url=None,
            attempts=attempts,
        )

    if not story_url:
        return ExtractionResult(
            method="hn_text" if hn_text else None,
            text=hn_text,
            source_url=None,
            final_url=None,
            content_type=None,
            url_type="hn_text",
            page_title=story.get("title"),
            meta_description=None,
            canonical_url=None,
            attempts=attempts,
        )

    if detect_url_type(story_url) == "github":
        github_content = await try_github_content(session, semaphore, story_url, attempts)
        if github_content:
            return ExtractionResult(
                method=github_content.method,
                text=github_content.text,
                source_url=story_url,
                final_url=story_url,
                content_type=github_content.content_type,
                url_type="github",
                page_title=github_content.page_title,
                meta_description=github_content.meta_description,
                canonical_url=story_url,
                attempts=attempts,
            )

    try:
        fetched = await fetch_bytes(session, semaphore, story_url)
    except Exception as exc:
        attempts.append(ExtractionAttempt(method="fetch_external_url", ok=False, error=str(exc)))
        return ExtractionResult(
            method="hn_text" if hn_text else None,
            text=hn_text,
            source_url=story_url,
            final_url=None,
            content_type=None,
            url_type=detect_url_type(story_url),
            page_title=story.get("title"),
            meta_description=None,
            canonical_url=None,
            attempts=attempts,
        )

    url_type = detect_url_type(fetched.final_url, fetched.content_type)
    attempts.append(ExtractionAttempt(method="fetch_external_url", ok=True, text_length=len(fetched.body)))

    pdf_text = try_pdf_extraction(fetched.body, fetched.content_type, fetched.final_url, attempts)
    if pdf_text:
        return ExtractionResult(
            method="pdfminer",
            text=pdf_text,
            source_url=story_url,
            final_url=fetched.final_url,
            content_type=fetched.content_type,
            url_type=url_type,
            page_title=story.get("title"),
            meta_description=None,
            canonical_url=fetched.final_url,
            attempts=attempts,
        )

    html_text = fetched.body.decode("utf-8", errors="replace")
    metadata = extract_html_metadata(html_text)
    extractors = [
        ("trafilatura", lambda: try_trafilatura(html_text, fetched.final_url, attempts)),
        ("readability", lambda: try_readability(html_text, attempts)),
        ("lxml_main_content", lambda: try_lxml_main_content(html_text, attempts)),
        ("meta_description", lambda: try_meta_description(metadata, attempts)),
    ]

    for method_name, extractor in extractors:
        text = extractor()
        if text:
            return ExtractionResult(
                method=method_name,
                text=text,
                source_url=story_url,
                final_url=fetched.final_url,
                content_type=fetched.content_type,
                url_type=url_type,
                page_title=metadata.get("page_title"),
                meta_description=metadata.get("meta_description"),
                canonical_url=metadata.get("canonical_url"),
                attempts=attempts,
            )

    return ExtractionResult(
        method="hn_text" if hn_text else None,
        text=hn_text,
        source_url=story_url,
        final_url=fetched.final_url,
        content_type=fetched.content_type,
        url_type=url_type,
        page_title=metadata.get("page_title"),
        meta_description=metadata.get("meta_description"),
        canonical_url=metadata.get("canonical_url"),
        attempts=attempts,
    )
