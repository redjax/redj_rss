from __future__ import annotations

from constants import (
    DB_DATABASE,
    DB_HOST,
    DB_PASSWORD,
    DB_PORT,
    DB_TYPE,
    DB_USERNAME,
    cache_conf,
)
import diskcache

from loguru import logger as log
from red_utils.diskcache_utils import (
    check_cache_key_exists,
    default_cache_conf,
    default_timeout_dict,
    get_val,
    new_cache,
    set_expire,
    set_val,
)
from red_utils.sqlalchemy_utils import (
    Base,
    create_base_metadata,
    get_engine,
    get_session,
    saPGConnection,
    saSQLiteConnection,
)

log.debug(f"Matching DB type to: {DB_TYPE}")
match DB_TYPE:
    case "sqlite":
        log.debug("Detected SQLite DB")
        db_config = saSQLiteConnection(database=DB_DATABASE)

    case "postgres":
        log.debug("Detected Postgres DB")
        db_config = saPGConnection(
            host=DB_HOST,
            username=DB_USERNAME,
            password=DB_PASSWORD,
            port=DB_PORT,
            database=DB_DATABASE,
        )
    case _:
        raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}")

engine = get_engine(connection=db_config, db_type=DB_TYPE, echo=True)
SessionLocal = get_session(engine=engine, autoflush=True)


def get_db():
    db = SessionLocal()

    # try:
    #     yield db
    # except Exception as exc:
    #     raise Exception(f"Unhandled exception getting database session. Details: {exc}")
    # finally:
    #     db.close()

    return db


def get_cache(conf: dict = cache_conf) -> diskcache.Cache:
    cache: diskcache.Cache = new_cache(cache_conf=conf)

    return cache
