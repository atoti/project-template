import sys
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import atoti as tt
import httpx
from atoti_jdbc import UserContentStorageConfig

from .config import Config
from .create_and_join_tables import create_and_join_tables
from .create_cubes import create_cubes
from .load_tables import load_tables
from .skeleton2 import SKELETON


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


@asynccontextmanager
async def start_session(
    *,
    config: Config,
    http_client: httpx.AsyncClient,
) -> AsyncGenerator[tt.Session]:
    """Start the session, declare the data model and load the initial data."""
    session_config = get_session_config(config)
    with tt.Session.start(session_config) as session, SKELETON.of(session):
        with tt.mapping_lookup(check=config.check_mapping_lookups):
            create_and_join_tables()
            create_cubes(session)
        await load_tables(session, config=config, http_client=http_client)
        yield session
