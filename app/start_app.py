from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, nullcontext

import httpx

from .config import Config
from .load_tables import load_tables
from .skeleton import Skeleton
from .start_session import start_session
from .util import run_periodically


@asynccontextmanager
async def start_app(*, config: Config) -> AsyncGenerator[Skeleton]:
    async with (
        httpx.AsyncClient() as http_client,
        start_session(config=config, http_client=http_client) as skeleton,
        run_periodically(
            lambda: load_tables(skeleton, config=config, http_client=http_client),
            period=config.data_refresh_period,
        )
        if config.data_refresh_period
        else nullcontext(),
    ):
        yield skeleton
