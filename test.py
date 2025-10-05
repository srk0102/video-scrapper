import requests
from tqdm import tqdm

def download_video(url: str, output_path: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://rce.ibomma.men/",
        "Range": "bytes=0-",
        "Accept": "*/*",
    }

    # Kick off the request
    resp = requests.get(url, headers=headers, stream=True, timeout=(5, 300))
    resp.raise_for_status()

    # Figure out total size in bytes
    total_bytes = int(
        resp.headers.get("Content-Range", "")
            .split("/")
            [-1]
        if "Content-Range" in resp.headers
        else resp.headers.get("Content-Length", 0)
    )

    # Open the file and wrap the write loop in tqdm
    with open(output_path, "wb") as f, tqdm(
        total=total_bytes,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        desc=output_path
    ) as bar:
        for chunk in resp.iter_content(chunk_size=1024 * 1024):
            if not chunk:
                continue
            f.write(chunk)
            bar.update(len(chunk))

    print(f"\n✅ Download complete: {output_path!r}")

if __name__ == "__main__":
    download_video(
        "https://my-bucket-s3-ap-east-amazonaws.erezinero.space/"
        "Samudrudu-Telugu-2025-yd4js.mp4",
        "Samudrudu-Telugu-2025.mp4"
    )
