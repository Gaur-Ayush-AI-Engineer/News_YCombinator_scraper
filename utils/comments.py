import asyncio
import os
from collections import deque
from typing import Any

import aiohttp

from utils.http_client import fetch_json
from utils.text_utils import clean_html_text, unix_time_to_iso


HN_BASE_URL = os.getenv("HN_BASE_URL", "https://hacker-news.firebaseio.com/v0").rstrip("/")


async def fetch_comment_item(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    comment_id: int,
    depth: int,
    parent_id: int | None,
) -> dict[str, Any] | None:
    """Fetch one HN comment item and normalize it, skipping deleted/dead/empty comments."""
    try:
        comment = await fetch_json(session, semaphore, f"{HN_BASE_URL}/item/{comment_id}.json")
    except Exception:
        return None

    if not comment or comment.get("deleted") or comment.get("dead"):
        return None

    text = clean_html_text(comment.get("text"))
    if not text:
        return None

    return {
        "id": comment.get("id"),
        "parent_id": parent_id,
        "by": comment.get("by"),
        "time": unix_time_to_iso(comment.get("time")),
        "depth": depth,
        "text": text,
        "reply_ids": comment.get("kids", []),
        "reply_count": len(comment.get("kids", [])),
    }


async def fetch_comments_for_story(
    session: aiohttp.ClientSession,
    semaphore: asyncio.Semaphore,
    story: dict[str, Any],
    max_comments: int,
    reply_depth: int,
) -> list[dict[str, Any]]:
    """Fetch comments for one story up to the configured count and reply depth."""
    queue = deque((comment_id, 0, story.get("id")) for comment_id in story.get("kids", []))
    comments: list[dict[str, Any]] = []

    while queue and len(comments) < max_comments:
        batch_size = min(max_comments - len(comments), len(queue), 20)
        batch = [queue.popleft() for _ in range(batch_size)]
        fetched_comments = await asyncio.gather(
            *(
                fetch_comment_item(session, semaphore, comment_id, depth, parent_id)
                for comment_id, depth, parent_id in batch
            )
        )

        for comment in fetched_comments:
            if not comment:
                continue

            comments.append(comment)
            if comment["depth"] < reply_depth:
                queue.extend(
                    (reply_id, comment["depth"] + 1, comment["id"])
                    for reply_id in comment["reply_ids"]
                )

            if len(comments) >= max_comments:
                break

    return comments
