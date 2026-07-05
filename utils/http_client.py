import asyncio
import ssl
from typing import Any

import aiohttp
import certifi

from utils.models import FetchResult


def build_ssl_context() -> ssl.SSLContext:
    """Create an SSL context using certifi's certificate bundle."""
    return ssl.create_default_context(cafile=certifi.where())


async def fetch_json(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    url: str,
) -> Any:
    """Fetch a URL as JSON while respecting the shared concurrency semaphore."""
    async with semaphore:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            response.raise_for_status()
            return await response.json()


async def fetch_bytes(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    url: str,
) -> FetchResult:
    """Fetch a URL as bytes and return body, content type, and final redirected URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 HN top stories content pipeline",
        "Accept": "text/html,application/xhtml+xml,application/xml,application/pdf;q=0.9,*/*;q=0.8",
    }

    async with semaphore:
        async with session.get(
            url,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=45),
            allow_redirects=True,
        ) as response:
            response.raise_for_status()
            return FetchResult(
                body=await response.read(),
                content_type=response.headers.get("content-type", ""),
                final_url=str(response.url),
            )
