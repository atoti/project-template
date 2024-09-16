from collections.abc import Generator
from contextlib import contextmanager, nullcontext

import atoti as tt

from .config import Config
from .load_tables import load_tables
from .start_session import start_session
from .util import run_periodically


@contextmanager
def start_app(*, config: Config) -> Generator[tt.Session, None, None]:
    with (
        start_session(config=config) as session,
        run_periodically(
            lambda: load_tables(session, config=config),
            period=config.data_refresh_period,
        )
        if config.data_refresh_period
        else nullcontext(),
    ):
        yield session
