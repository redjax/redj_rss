from __future__ import annotations

import uuid

from .models import RPILocatorEntryModel
from .schemas import RPILocatorEntry, RPILocatorEntryCreate

from lib.parse_pydantic_schema import parse_pydantic_schema
from loguru import logger as log
from sqlalchemy import func, select
from sqlalchemy.orm import Query, Session

def validate_db(db: Session = None) -> Session:
    if not db:
        raise ValueError("Missing DB Session object")

    if not isinstance(db, Session):
        raise TypeError(
            f"Invalid type for db: ({type(db)}). Must be of type sqlalchemy.orm.Session"
        )

    return db


def create(
    obj: RPILocatorEntryCreate = None, db: Session = None
) -> RPILocatorEntryModel:
    validate_db(db)

    log.debug(f"Create obj: ({type(obj)}): {obj}")

    try:
        with db as sess:
            db_obj: RPILocatorEntryModel | None = None

            db_obj_sel = select(RPILocatorEntryModel).where(
                RPILocatorEntryModel.title == obj.title
            )
            log.info(f"Checking for existence of {obj.title} in database")
            db_obj = sess.execute(db_obj_sel).first()

            log.debug(f"Results ({type(db_obj)}): {db_obj}")

            if db_obj:
                log.info(f"Found object in database. Returning instead of committing.")
                return db_obj
            else:
                log.info(
                    f"Did not find object in database. Committing object to database."
                )

                log.debug("Dumping schema to dict")
                dump_schema: dict = parse_pydantic_schema(schema=obj)
                new_obj: RPILocatorEntryModel = RPILocatorEntryModel(
                    title=dump_schema["title"],
                    author=dump_schema["author"],
                    link=dump_schema["link"],
                    entry_id=dump_schema["entry_id"],
                    published=dump_schema["published"],
                )

                sess.add(new_obj)
                sess.commit()

                return new_obj

    except Exception as exc:
        log.error(
            Exception(f"Unhandled exception writing object to database. Details: {exc}")
        )

        return False
