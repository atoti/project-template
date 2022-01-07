from __future__ import annotations

from types import TracebackType
from typing import Optional, Type

import atoti as tt

from .config import Config
from .load_tables import load_tables
from .start_session import start_session
from .util import run_periodically


class App:
    """Regroup the session with other resources so that they can be closed together."""

    def __init__(self, *, config: Config) -> None:
        # The config is kept private to deter passing an App to functions when a Config is all they need.
        self._session = start_session(config=config)
        self._stop_refreshing_data = (
            run_periodically(
                lambda: load_tables(self.session, config=config),
                period=config.data_refresh_period,
            )
            if config.data_refresh_period
            else None
        )

    @property
    def session(self) -> tt.Session:
        return self._session

    def close(self) -> None:
        if self._stop_refreshing_data:
            self._stop_refreshing_data()
        self.session.close()

    def __enter__(self) -> App:
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.close()
