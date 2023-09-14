from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any, List, Optional
import uuid

from loguru import logger as log
from red_utils.sqlalchemy_utils import Base
from red_utils.sqlalchemy_utils.custom_types import CompatibleUUID
import sqlalchemy as sa

from sqlalchemy import Column, ForeignKey, Table
import sqlalchemy.orm as sa_orm
from sqlalchemy.orm import Mapped, Session, mapped_column, relationship
from sqlalchemy.sql import func

class UUIDMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, insert_default=uuid.uuid4
    )


class RPILocatorEntryModelBase(Base, UUIDMixin):
    __abstract__ = True
    __tablename__ = "rpiLocator"

    type_annotation_map = {uuid.UUID: CompatibleUUID}

    # id: Mapped[uuid.UUID] = mapped_column(
    #     primary_key=True, index=True, insert_default=uuid.uuid4
    # )

    published: Mapped[datetime | None] = mapped_column(sa.DateTime)
    entry_id: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    title: Mapped[str | None] = mapped_column(sa.String, index=True, nullable=True)
    summary: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    author: Mapped[str | None] = mapped_column(sa.String, index=True, nullable=True)
    link: Mapped[str | None] = mapped_column(sa.String, nullable=True)


class RPILocatorEntryModel(RPILocatorEntryModelBase):
    # __tablename__ = "rpiLocator"

    # type_annotation_map = {uuid.UUID: CompatibleUUID}

    # id: Mapped[uuid.UUID] = mapped_column(
    #     primary_key=True, index=True, insert_default=uuid.uuid4
    # )

    # published: Mapped[datetime | None] = mapped_column(sa.DateTime)
    # entry_id: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    # title: Mapped[str | None] = mapped_column(sa.String, index=True, nullable=True)
    # summary: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    # author: Mapped[str | None] = mapped_column(sa.String, index=True, nullable=True)
    # link: Mapped[str | None] = mapped_column(sa.String, nullable=True)

    title_detail: Mapped["RPILocatorTitleDetailModel"] = relationship(
        back_populates="entry"
    )


class RPILocatorTitleDetailModelBase(Base, UUIDMixin):
    __abstract__ = True
    __tablename__ = "titleDetail"

    type_annotation_map = {uuid.UUID: CompatibleUUID}

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, insert_default=uuid.uuid4
    )

    type: Mapped[str | None] = mapped_column(sa.String, index=True, nullable=True)
    language: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    base: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    value: Mapped[str | None] = mapped_column(sa.String, nullable=True)


class RPILocatorTitleDetailModel(RPILocatorTitleDetailModelBase):
    # __tablename__ = "titleDetail"

    # id: Mapped[uuid.UUID] = mapped_column(
    #     primary_key=True, index=True, insert_default=uuid.uuid4
    # )

    # type: Mapped[str | None] = mapped_column(sa.String, index=True, nullable=True)
    # language: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    # base: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    # value: Mapped[str | None] = mapped_column(sa.String, nullable=True)

    entry_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("rpiLocator.id"))
    entry: Mapped["RPILocatorEntryModel"] = relationship(back_populates="title_detail")
