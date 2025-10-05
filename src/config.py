from pydantic import BaseSettings, Field
from typing import List

class Settings(BaseSettings):
    # Cloudflare R2 / S3
    r2_endpoint: str = Field(..., env="R2_ENDPOINT")
    r2_access_key: str = Field(..., env="R2_ACCESS_KEY")
    r2_secret_key: str = Field(..., env="R2_SECRET_KEY")
    r2_bucket: str     = Field(..., env="R2_BUCKET")

    # Concurrency & retries
    max_concurrent: int   = Field(50, env="MAX_CONCURRENT")
    max_retries: int      = Field(5, env="MAX_RETRIES")
    initial_backoff: float = Field(1.0, env="INITIAL_BACKOFF")

    # Proxy & UA pools
    proxies: List[str]     = Field([], env="PROXIES")
    user_agents: List[str] = Field([], env="USER_AGENTS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
