from __future__ import annotations

import json
import random
import sys
import msgpack

## Appends the src/ dir at ../ to Python's path
#  Allows accessing files in i.e. ../.serialize
sys.path.append(".")

from typing import Union

from constants import CONTAINER_ENV, ENV, FEED_URL, settings
from dependencies import (
    check_cache_key_exists,
    get_cache,
    get_val,
    set_expire,
    set_val,
    default_cache_conf,
    cache_conf,
)
from domain.rss.schemas import FeedEntry, RPILocatorEntry
import feedparser

from loguru import logger as log
from red_utils.loguru_utils import default_color_fmt, init_logger
from utils.rss_utils import get_feed, select_random_entry

import polars as pl

loguru_console_sink: dict = {
    "sink": sys.stderr,
    "format": default_color_fmt,
    "level": settings.LOG_LEVEL,
    "colorize": True,
}

log.remove()
log.add(**loguru_console_sink)


def debug_feed(feed: feedparser.FeedParserDict = None) -> None:
    log.debug(f"Feed type: {feed.version}")

    log.debug(f"Feed title: [{feed.feed.title}]")
    log.debug(f"Feed link: {feed.feed.link}")


if __name__ == "__main__":
    log.info(f"[env:{ENV}|container:{CONTAINER_ENV}] Feed URL: {FEED_URL}")

    log.debug(f"Cache conf: {cache_conf}")

    ## Create a diskcache to avoid being rate limited.
    cache = get_cache()

    ## Get feed results. If previous results exist in cache,
    #  use those. Pass USE_CACHE=False to disable cache check.
    _feed = get_feed(cache=cache, use_cache=True)
    # log.debug(f"Feed: ({type(dict(_feed))}): {_feed}")

    log.info(f"Found ({len(_feed.entries)}) entries")

    rand_entry_dict = select_random_entry(_feed.entries)

    entries: list[RPILocatorEntry] = []

    for _entry in _feed.entries:
        entry: RPILocatorEntry = RPILocatorEntry(**_entry)
        entries.append(entry)
