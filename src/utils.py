import random
import string
from itertools import cycle
from typing import Optional
from config import settings

# cycle through your proxies (if any)
_proxy_cycle = cycle(settings.proxies)
def get_proxy() -> Optional[str]:
    return next(_proxy_cycle) if settings.proxies else None

# pick a random UA
def get_user_agent() -> str:
    return random.choice(settings.user_agents) if settings.user_agents else \
           "Mozilla/5.0 (compatible; VideoScraper/1.0)"

# generate a unique R2 key
def generate_object_key(page_url: str) -> str:
    base = page_url.rstrip("/").split("/")[-1] or "video"
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{base}-{suffix}.mp4"
