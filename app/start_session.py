import sys
from typing import Any, Dict

import atoti as tt
from pydantic import AnyUrl

from .config import Config
from .create_and_join_tables import create_and_join_tables
from .create_cubes import create_cubes
from .load_tables import load_tables


def create_session(*, config: Config) -> tt.Session:
    session_config: Dict[str, Any] = {
        "logging": {"destination": sys.stdout},
    }

    if config.port is not None:
        session_config["port"] = config.port

    if config.user_content_storage:
        session_config["user_content_storage"] = (
            {"url": str(config.user_content_storage)}
            if isinstance(config.user_content_storage, AnyUrl)
            else config.user_content_storage
        )

    return tt.create_session(config=session_config)


def start_session(*, config: Config) -> tt.Session:
    """Start the session, declare the data model and load the initial data."""
    session = create_session(config=config)
    create_and_join_tables(session)
    create_cubes(session)
    load_tables(session, config=config)
    return session
