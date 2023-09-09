from __future__ import annotations

from datetime import date, datetime
from time import mktime, struct_time
from typing import Any, Optional, Union
import uuid

import feedparser
import pendulum

from pydantic import BaseModel, Field, ValidationError, validator


class FeedEntryBase(BaseModel):
    title: str | None = Field(default=None)
    link: str | None = Field(default=None)
    author: str | None = Field(default=None)
    entry_id: str | None = Field(default=None)
    image: dict | None = Field(default=None)
    categories: list | None = Field(default=None)

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
    published_parsed: struct_time | None = Field(default=None)
