import asyncio
import random
import logging
from extractor import get_video_stream_url
from downloader import fetch_video_stream
from uploader import upload_stream_to_r2
from utils import generate_object_key
from config import settings

logger = logging.getLogger(__name__)

async def process_video(page_url: str):
    backoff = settings.initial_backoff
    for attempt in range(1, settings.max_retries + 1):
        try:
            # resolve direct stream URL (offload sync call)
            loop = asyncio.get_event_loop()
            video_url = await loop.run_in_executor(None, get_video_stream_url, page_url)

            key = generate_object_key(page_url)
            # fetch & upload in one pass
            stream = fetch_video_stream(video_url)
            await upload_stream_to_r2(stream, key)

            logger.info(f"✓ {page_url} → {key}")
            return key
        except Exception as e:
            logger.warning(f"Attempt {attempt} failed for {page_url}: {e}")
            if attempt >= settings.max_retries:
                logger.error(f"✗ Giving up on {page_url}")
                raise
            await asyncio.sleep(backoff + random.random())
            backoff *= 2

async def run_batch(urls: list[str]):
    sem = asyncio.Semaphore(settings.max_concurrent)
    async def guarded(url):
        async with sem:
            return await process_video(url)

    return await asyncio.gather(*(guarded(u) for u in urls), return_exceptions=True)
