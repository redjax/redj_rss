from __future__ import annotations

from dynaconf import settings

ENV: str = settings.ENV
CONTAINER_ENV: bool = settings.CONTAINER_ENV
FEED_URL: str = settings.FEED_URL

DB_TYPE: str | None = settings.DB_TYPE or None
DB_HOST: str | None = settings.DB_HOST or None
DB_USERNAME: str | None = settings.DB_USERNAME or None
DB_PASSWORD: str | None = settings.DB_PASSWORD or None
DB_PORT: int | None = settings.DB_PORT or None
DB_DATABASE: str | None = settings.DB_DATABASE or None

# cache_conf: dict = settings.CACHE_CONF or {"directory": ".cache", "timeout": 900}
cache_conf = {"directory": ".cache", "timeout": 300}
