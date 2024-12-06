import asyncio
from urllib.parse import urlparse

from . import Config, start_app


async def main() -> None:
    async with start_app(config=Config()) as session:
        port = urlparse(session.url).port or 80
        print(f"Session listening on port {port}")
        await asyncio.to_thread(session.wait)


asyncio.run(main())
