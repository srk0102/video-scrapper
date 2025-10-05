import sys
import asyncio
import logging
from tasks import run_batch

logging.basicConfig(level=logging.INFO)

def load_urls(path: str) -> list[str]:
    with open(path) as f:
        return [l.strip() for l in f if l.strip()]

async def main():
    if len(sys.argv) == 3 and sys.argv[1] == "--file":
        urls = load_urls(sys.argv[2])
    elif len(sys.argv) > 1:
        urls = sys.argv[1:]
    else:
        print("Usage: python main.py [URL ...]  OR  python main.py --file urls.txt")
        return

    results = await run_batch(urls)
    success = sum(1 for r in results if isinstance(r, str))
    fail    = len(results) - success
    logging.info(f"Completed: {success} succeeded, {fail} failed")

if __name__ == "__main__":
    asyncio.run(main())
