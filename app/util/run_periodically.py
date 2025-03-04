import asyncio
from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager


@asynccontextmanager
async def run_periodically(
    callback: Callable[[], Awaitable[None]],
    /,
    *,
    period: float,
) -> AsyncGenerator[None]:
    stopped = asyncio.Event()

    async def loop() -> None:
        while not stopped.is_set():
            await callback()
            await asyncio.sleep(period)

    task = asyncio.create_task(loop())

    try:
        yield
    finally:
        stopped.set()
        await task
