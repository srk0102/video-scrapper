import aiohttp
from typing import AsyncIterator
from config import settings
from utils import get_proxy, get_user_agent

async def fetch_video_stream(url: str) -> AsyncIterator[bytes]:
    """
    Yields chunks of the video at `url`, using optional proxy/UA rotation.
    """
    proxy = get_proxy()
    headers = {
        "User-Agent": get_user_agent(),
        "Cache-Control": "no-cache, no-store, must-revalidate",
    }
    timeout = aiohttp.ClientTimeout(total=None, sock_connect=30, sock_read=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=headers, proxy=proxy) as resp:
            resp.raise_for_status()
            async for chunk in resp.content.iter_chunked(64 * 1024):
                yield chunk
