from __future__ import annotations

import diskcache

from loguru import logger as log
from red_utils.diskcache_utils import (
    check_cache_key_exists,
    default_cache_conf,
    default_timeout_dict,
    get_val,
    new_cache,
    set_expire,
    set_val,
)

from constants import cache_conf


def get_cache(conf: dict = cache_conf) -> diskcache.Cache:
    cache: diskcache.Cache = new_cache(cache_conf=conf)

    return cache
