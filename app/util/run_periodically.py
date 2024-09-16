from collections.abc import Callable, Generator
from contextlib import contextmanager
from datetime import timedelta
from threading import Event, Thread


@contextmanager
def run_periodically(
    callback: Callable[[], None], /, *, daemon: bool | None = None, period: timedelta
) -> Generator[None, None, None]:
    period_in_seconds = period.total_seconds()
    stopped = Event()

    def loop() -> None:
        while not stopped.wait(period_in_seconds):
            callback()

    Thread(target=loop, daemon=daemon).start()

    yield

    stopped.set()
