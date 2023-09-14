from __future__ import annotations

import uuid

from .models import RPILocatorEntryModel
from .schemas import RPILocatorEntry, RPILocatorEntryCreate, RPILocatorFieldDetailCreate

from lib.parse_pydantic_schema import parse_schema
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


def count_objects(db: Session = None) -> int:
    """Count number of objects in database."""
    validate_db(db)

    try:
        with db as sess:
            rpi_locator_count = sess.query(func.count(RPILocatorEntryModel.id)).scalar()

            return rpi_locator_count

    except Exception as exc:
        log.error(
            f"Unhandled exception getting count of Products in database. Details: {exc}"
        )
        return False


def create(
    obj: RPILocatorEntryCreate = None, db: Session = None
) -> RPILocatorEntryModel:
    """Commit object to database."""
    validate_db(db)

    # log.debug(f"Create obj: ({type(obj)}): {obj}")

    try:
        with db as sess:
            db_obj: RPILocatorEntryModel | None = None

            db_obj_sel = select(RPILocatorEntryModel).where(
                RPILocatorEntryModel.title == obj.title
            )
            # log.info(f"Checking for existence of {obj.title} in database")
            db_obj = sess.execute(db_obj_sel).first()

            # log.debug(f"Results ({type(db_obj)}): {db_obj}")

            if db_obj:
                # log.info(f"Found object in database. Returning instead of committing.")
                return db_obj
            else:
                # log.info(
                # f"Did not find object in database. Committing object to database."
                # )

                log.debug("Dumping schema to dict")
                dump_schema: dict = parse_schema(schema=obj)
                log.debug(
                    f"Title detail ({type(dump_schema['title_detail'])}): {dump_schema['title_detail']}"
                )
                new_rpilocator_obj: RPILocatorEntryModel = RPILocatorEntryModel(
                    title=dump_schema["title"],
                    author=dump_schema["author"],
                    link=dump_schema["link"],
                    entry_id=dump_schema["entry_id"],
                    published=dump_schema["published"],
                    summary=dump_schema["summary"],
                )

                sess.add(new_rpilocator_obj)
                sess.commit()
                sess.refresh(new_rpilocator_obj)

                return new_rpilocator_obj

    except Exception as exc:
        log.error(
            Exception(f"Unhandled exception writing object to database. Details: {exc}")
        )

        return False


def get_all(db: Session = None) -> list[RPILocatorEntryModel]:
    validate_db(db)

    try:
        with db as sess:
            all_rpi_locators = sess.query(RPILocatorEntryModel).all()

            return all_rpi_locators

    except Exception as exc:
        log.error(
            Exception(
                f"Unhandled exception retrieving all objects from database. Details: {exc}"
            )
        )

        return False


def delete_all(db: Session = None) -> bool:
    """Delete all objects from database."""
    validate_db(db)

    log.warning("Deleting all objects from database")

    try:
        with db as sess:
            db_objects = sess.query(RPILocatorEntryModel).all()

            if not db_objects:
                log.warning(f"No objects found in database")

                return False

            for obj in db_objects:
                sess.delete(obj)

            sess.commit()

            return db_objects

    except Exception as exc:
        log.error(
            Exception(
                f"Unhandled exception deleting all objects from database. Details: {exc}"
            )
        )

        return False
