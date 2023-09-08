from __future__ import annotations

import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from pathlib import Path
import random
import sys

import json
from typing import Union

from constants import CONTAINER_ENV, ENV, FEED_URL
from dependencies import (
    check_cache_key_exists,
    get_cache,
    get_val,
    set_expire,
    set_val,
    get_db,
    create_base_metadata,
)
from dependencies import cache_conf, default_cache_conf, Base, engine

from domain.rss import FeedEntry, RPILocatorEntry, RPILocatorEntryModel
from dynaconf import settings
import feedparser

from loguru import logger as log
from red_utils.loguru_utils import default_color_fmt, init_logger
from utils.rss_utils import get_feed, select_random_entry

loguru_console_sink: dict = {
    "sink": sys.stderr,
    "format": default_color_fmt,
    "level": settings.LOG_LEVEL,
    "colorize": True,
}

log.remove()
log.add(**loguru_console_sink)

create_base_metadata(base_obj=Base(), engine=engine)


def debug_feed(feed: feedparser.FeedParserDict = None) -> None:
    log.debug(f"Feed type: {feed.version}")

    log.debug(f"Feed title: [{feed.feed.title}]")
    log.debug(f"Feed link: {feed.feed.link}")


def parse_entries_to_objs(entries: list[dict] = []) -> list[RPILocatorEntry]:
    """Accept a list of dict objects to convert to instances of RPILocatorEntry."""
    entries: list[RPILocatorEntry] = []

    for _entry in _feed.entries:
        try:
            entry: RPILocatorEntry = RPILocatorEntry(**_entry)
        except Exception as exc:
            log.error(
                Exception(
                    f"Unhandled exception converting dict to RPILocatorEntry object. Details: {exc}"
                )
            )
            pass

        entries.append(entry)

    return entries


if __name__ == "__main__":
    log.info(f"[env:{ENV}|container:{CONTAINER_ENV}] Feed URL: {FEED_URL}")

    ## Create a diskcache to avoid being rate limited.
    cache = get_cache()

    ## Get feed results. If previous results exist in cache,
    #  use those. Pass USE_CACHE=False to disable cache check.
    _feed = get_feed(cache=cache, use_cache=True)

    log.info(f"Found ({len(_feed.entries)}) entries")

    rand_entry_dict = select_random_entry(_feed.entries)

    entries = parse_entries_to_objs(entries=_feed.entries)
    log.debug(f"Converted [{len(entries)}] objects to RPILocatorEntry class.")
