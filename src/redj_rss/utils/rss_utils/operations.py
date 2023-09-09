from __future__ import annotations

import json
import random

from typing import Union

from constants import settings
from dependencies import check_cache_key_exists, get_val, set_val
import diskcache
import feedparser

from loguru import logger as log
import pendulum
from red_utils.msgpack_utils import (
    default_serialize_dir,
    msgpack_deserialize,
    msgpack_deserialize_file,
    msgpack_serialize,
    msgpack_serialize_file,
)


def serialize_feed_res(
    data: feedparser.FeedParserDict = None, name: str = None
) -> dict:
    try:
        _data = {}

        for k, v in data.items():
            _data[k] = v

    except Exception as exc:
        log.error(
            Exception(
                f"Unhandled exception dumping data to serializable string. Details: {exc}"
            )
        )

        return False

    ts = pendulum.now().format("YY-MM-DD_HH:mm")
    filename: str = f"{ts}_{name}"

    _ser = msgpack_serialize_file(_json=_data, filename=filename)

    return _ser


def get_feed(
    url: str = settings.FEED_URL,
    cache: diskcache.Cache = None,
    use_cache: bool = True,
    cache_expire: int = settings.CACHE_CONF.timeout,
) -> feedparser.FeedParserDict:
    """Retrieve an RSS feed URL's contents."""
    if not url:
        raise ValueError("Missing a feed URL")

    if cache is None:
        if use_cache:
            raise ValueError("Missing a cache object.")

    try:
        log.info(f"Getting feed [{url}]")

        if use_cache:
            with cache as client:
                if not check_cache_key_exists(key=url, cache=client):
                    log.debug("Cached: False")
                    _feed: feedparser.FeedParserDict = feedparser.parse(url)

                    set_val(
                        cache=client, key=url, val=_feed.copy(), expire=cache_expire
                    )
                else:
                    log.debug(f"Cache: True")
                    cached_feed = get_val(key=url, cache=client)
                    _feed: feedparser.FeedParserDict = feedparser.FeedParserDict(
                        **cached_feed
                    )
        else:
            log.debug("Cached: False")
            _feed: feedparser.FeedParserDict = feedparser.parse(url)

        # serialize = serialize_feed_res(data=_feed, name=_feed.feed.title)
        # log.debug(f"Serialized: {serialize}")

        return _feed

    except Exception as exc:
        raise Exception(
            f"Unhandled exception getting feed from URL: {url}. Detail: {exc}"
        )


def select_random_entry(
    entries: list[feedparser.FeedParserDict] = [],
) -> dict[str, Union[int, feedparser.FeedParserDict]]:
    """Generate a random number between 0 and the length of input entries list.

    Select a random item from the list using the random number as an index.
    """
    if entries is None:
        raise ValueError("List of entries is missing or empty")

    list_len: int = len(entries)
    rand_index: int = random.randint(0, list_len - 1)

    rand_item = entries[rand_index]

    return_item = {"index": rand_index, "item": rand_item}

    return return_item
