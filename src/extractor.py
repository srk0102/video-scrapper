import logging
from yt_dlp import YoutubeDL
from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

def extract_with_ytdlp(url: str) -> str:
    opts = {"format": "best", "noplaylist": True, "quiet": True, "skip_download": True}
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    # pick the best format URL
    formats = info.get("formats") or []
    if formats:
        return formats[-1]["url"]
    return info.get("url")

def extract_with_playwright(url: str, selector: str = "video") -> str:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(selector, timeout=30_000)
        elem = page.query_selector(selector)
        src = elem.get_attribute("src") if elem else None
        browser.close()
    if not src:
        raise RuntimeError(f"No <video> src found at {url}")
    return src

def get_video_stream_url(url: str) -> str:
    try:
        return extract_with_ytdlp(url)
    except Exception as e:
        logger.warning(f"yt_dlp failed for {url}: {e}")
    return extract_with_playwright(url)
