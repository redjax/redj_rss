from __future__ import annotations

from dynaconf import settings

ENV: str = settings.ENV
CONTAINER_ENV: bool = settings.CONTAINER_ENV
FEED_URL: str = settings.FEED_URL

cache_conf: dict = settings.CACHE_CONF or {"directory": ".cache", "timeout": 900}
