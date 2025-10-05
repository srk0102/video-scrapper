import aioboto3
from botocore.config import Config
from typing import AsyncIterator
from config import settings

async def upload_stream_to_r2(
    stream: AsyncIterator[bytes],
    key: str,
    content_type: str = None
):
    session = aioboto3.Session()
    async with session.client(
        "s3",
        endpoint_url=settings.r2_endpoint,
        aws_access_key_id=settings.r2_access_key,
        aws_secret_access_key=settings.r2_secret_key,
        config=Config(signature_version="s3v4")
    ) as s3:
        params = {
            "Bucket": settings.r2_bucket,
            "Key": key,
            "Body": stream,
        }
        if content_type:
            params["ContentType"] = content_type
        await s3.put_object(**params)
