# coding: utf-8

"""
Contains database schema upgrade rutines for bookworm 
"""

import sqlalchemy as sa
from db_magic.schema_upgrades import perform_upgrade
import bookworm.typehints as t
from bookworm.logger import logger

log = logger.getChild(__name__)
CURRENT_SCHEMA_VERSION = 1


def get_upgrades() -> t.Dict[int, t.Tuple[t.Callable]]:
    return {
        1: (v1_schema_upgrade,),
    }


def upgrade_database_schema(session):
    perform_upgrade(
        session, upgrades=get_upgrades(), schema_version=CURRENT_SCHEMA_VERSION
    )


def v1_schema_upgrade(session, connection):
    """Upgrade to schema version 1, effective since Bookworm v0.2b1."""
    # Book table contains only book identifier and title
    connection.execute("""CREATE TABLE new_book
        id INTEGER NOT NULL,
        identifier VARCHAR(512) NOT NULL,
        title VARCHAR(512) NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (identifier))
    """)
    