from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from time import mktime, struct_time
from typing import Any, Optional, Union
import uuid

import pendulum
import feedparser

from pydantic import BaseModel, Field, ValidationError, validator


class FeedEntryBase(BaseModel):
    title: str | None = field(default=None)
    link: str | None = field(default=None)
    author: str | None = field(default=None)
    entry_id: str | None = field(default=None)
    image: dict | None = field(default=None)
    categories: list | None = field(default=None)

    @property
    def has_title(self) -> bool:
        return [True if self.title else False]

    @property
    def has_link(self) -> bool:
        return [True if self.link else False]

    @property
    def has_author(self) -> bool:
        return [True if self.author else False]

    @property
    def has_published_date(self) -> bool:
        return [True if self.published else False]

    @property
    def has_entry_id(self) -> bool:
        return [True if self.entry_id else False]

    @property
    def has_image(self) -> bool:
        return [True if self.image else False]

    @property
    def has_categories(self) -> bool:
        return [True if self.categories else False]

    class Config:
        arbitrary_types_allowed = True


class FeedEntry(FeedEntryBase):
    published_parsed: struct_time | None = field(default=None)


class RPILocatorEntry(FeedEntryBase):
    title_detail: dict | None = field(default=None)
    summary: str | None = field(default=None)
    summary_detail: dict | None = field(default=None)
    links: list[dict] | None = field(default=None)
    link: str | None = field(default=None)
    tags: list[dict] | None = field(default=None)
    id: str | None = field(default=None)
    guidislink: bool = field(default=False)
    published: datetime | None = field(default=None)

    @property
    def is_in_stock(self) -> bool:
        return [True if "is In Stock at" in self.title else False]

    @validator("published", pre=True)
    def validatae_published(cls, v) -> datetime:
        """Convert the published timestamp string to a datetime.

        An entry's format is: "ddd, DD MMM YYYY HH:mm:ss z". Uses pendulum
        for formatting:

        https://pendulum.eustace.io/docs/#tokens
        """
        ##
        published_fmt: str = "ddd, DD MMM YYYY HH:mm:ss z"
        dt = pendulum.from_format(v, fmt=published_fmt)

        return dt
