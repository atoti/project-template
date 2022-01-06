from datetime import timedelta
from threading import Event, Thread
from typing import Callable, Optional


def run_periodically(
    callback: Callable[[], None], *, daemon: Optional[bool] = None, period: timedelta
) -> Callable[[], None]:
    period_in_seconds = period.total_seconds()
    stopped = Event()

    def loop() -> None:
        while not stopped.wait(period_in_seconds):
            callback()

    Thread(target=loop, daemon=daemon).start()

    return stopped.set
