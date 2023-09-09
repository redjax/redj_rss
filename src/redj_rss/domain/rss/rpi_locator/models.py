from typing import Any, Optional, List

import uuid

from datetime import datetime, date, timedelta

from red_utils.sqlalchemy_utils import Base
from red_utils.sqlalchemy_utils.custom_types import CompatibleUUID

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from sqlalchemy.sql import func

from sqlalchemy.orm import Session, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column

from decimal import Decimal

from loguru import logger as log


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
