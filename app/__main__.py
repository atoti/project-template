from asyncio import run, to_thread
from urllib.parse import urlparse

from . import Config, start_app


async def main() -> None:
    async with start_app(config=Config()) as session:
        port = urlparse(session.url).port or 80
        print(f"Session listening on port {port}")  # noqa: T201
        await to_thread(session.wait)


run(main())
