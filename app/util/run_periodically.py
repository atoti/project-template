import asyncio
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from datetime import timedelta


@asynccontextmanager
async def run_periodically(
    callback: Callable[[], Awaitable[None]],
    /,
    *,
    period: timedelta,
) -> AsyncGenerator[None]:
    period_in_seconds = period.total_seconds()
    stopped = asyncio.Event()

    async def loop() -> None:
        while not stopped.is_set():
            await callback()
            await asyncio.sleep(period_in_seconds)

    task = asyncio.create_task(loop())

    try:
        yield
    finally:
        stopped.set()
        await task
