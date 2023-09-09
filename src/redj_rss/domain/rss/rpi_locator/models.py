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

class RPILocatorEntryModel(Base):
    __tablename__ = "rpilocator"

    type_annotation_map = {uuid.UUID: CompatibleUUID}

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, index=True, insert_default=uuid.uuid4
    )

    title: Mapped[str | None] = mapped_column(sa.String, index=True, nullable=True)
    link: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    author: Mapped[str | None] = mapped_column(sa.String, index=True, nullable=True)
    entry_id: Mapped[str | None] = mapped_column(sa.String, nullable=True)
    published: Mapped[datetime | None] = mapped_column(sa.DateTime)
