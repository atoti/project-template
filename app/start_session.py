import sys
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import atoti as tt
from atoti_jdbc import UserContentStorageConfig

from .config import Config
from .create_and_join_tables import create_and_join_tables
from .create_cubes import create_cubes
from .load_tables import load_tables


def get_session_config(config: Config, /) -> tt.SessionConfig:
    user_content_storage: Path | UserContentStorageConfig | None = None

    if config.user_content_storage is not None:
        user_content_storage = (
            config.user_content_storage
            if isinstance(config.user_content_storage, Path)
            else UserContentStorageConfig(url=str(config.user_content_storage))
        )

    return tt.SessionConfig(
        logging=tt.LoggingConfig(destination=sys.stdout),
        port=config.port,
        user_content_storage=user_content_storage,
    )


@contextmanager
def start_session(*, config: Config) -> Generator[tt.Session, None, None]:
    """Start the session, declare the data model and load the initial data."""
    session_config = get_session_config(config)
    with tt.Session.start(session_config) as session:
        create_and_join_tables(session)
        create_cubes(session)
        load_tables(session, config=config)
        yield session
