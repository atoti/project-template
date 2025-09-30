from asyncio import Event, create_task, sleep
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager


@asynccontextmanager
async def run_periodically(
    callback: Callable[[], Awaitable[None]],
    /,
    *,
    period: float,
) -> AsyncGenerator[None]:
    stopped = Event()

    async def loop() -> None:
        while not stopped.is_set():
            await callback()
            await sleep(period)

    task = create_task(loop())

    try:
        yield
    finally:
        stopped.set()
        await task
