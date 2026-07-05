import asyncio
import os
from typing import Any

import aiohttp

from utils.http_client import fetch_json


HN_BASE_URL = os.getenv("HN_BASE_URL", "https://hacker-news.firebaseio.com/v0").rstrip("/")


async def fetch_top_stories(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    story_limit: int,
) -> list[dict[str, Any]]:
    """Fetch the current top HN story IDs and then fetch each story item."""
    top_story_ids = await fetch_json(session, semaphore, f"{HN_BASE_URL}/topstories.json")
    top_story_ids = top_story_ids[:story_limit]
    stories = await asyncio.gather(
        *(
            fetch_json(session, semaphore, f"{HN_BASE_URL}/item/{story_id}.json")
            for story_id in top_story_ids
        )
    )
    return [story for story in stories if story]
