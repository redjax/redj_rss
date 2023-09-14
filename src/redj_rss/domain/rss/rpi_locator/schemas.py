from __future__ import annotations

from datetime import date, datetime
from time import mktime, struct_time
from typing import Any, Optional, Union
import uuid

from ..schemas import FeedEntryBase

import feedparser
import pendulum

from pydantic import BaseModel, Field, ValidationError, validator


class RPILocatorFieldDetail(BaseModel):
    type: str | None = Field(default="text/plain")
    language: str | None = Field(default=None)
    base: str | None = Field(default=None)
    value: str | None = Field(default=None)

    class Meta:
        orm_model = "RPILocatorTitleDetail"


class RPILocatorFieldDetailCreate(RPILocatorFieldDetail):
    id: uuid.UUID

    class Config:
        from_attributes = True


class RPILocatorLink(BaseModel):
    rel: str | None = Field(default=None)
    type: str | None = Field(default=None)
    href: str | None = Field(default=None)


class RPILocatorTag(BaseModel):
    term: str | None = Field(default=None)
    scheme: str | None = Field(default=None)
    label: str | None = Field(default=None)


class RPILocatorEntryBase(FeedEntryBase):
    # title_detail: dict | None = Field(default=None)
    title_detail: RPILocatorFieldDetail | None = Field(default=None)
    summary: str | None = Field(default=None)
    # summary_detail: dict | None = Field(default=None)
    summary_detail: RPILocatorFieldDetail | None = Field(default=None)
    # links: list[dict] | None = Field(default=None)
    links: list[RPILocatorLink] | None = Field(default=None)
    link: str | None = Field(default=None)
    # tags: list[dict] | None = Field(default=None)
    tags: list[RPILocatorTag] | None = Field(default=None)
    entry_id: str | None = Field(default=None, alias="id")
    guidislink: bool = Field(default=False)
    published: datetime | None = Field(default=None)

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

    class Meta:
        orm_model = "RPILocatorEntryModel"


class RPILocatorEntryCreate(RPILocatorEntryBase):
    id: uuid.UUID
    title_detail: RPILocatorFieldDetailCreate | None = Field(default=None)

    class Config:
        from_attributes = True


class RPILocatorEntryUpdate(RPILocatorEntryBase):
    id: uuid.UUID | None = None

    class Config:
        from_attributes = True


class RPILocatorEntry(RPILocatorEntryBase):
    pass
