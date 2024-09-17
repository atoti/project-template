from urllib.parse import urlparse

from . import Config, start_app

with start_app(config=Config()) as session:
    port = urlparse(session.url) or 80
    print(f"Session listening on port {port}")  # noqa: T201
    session.wait()
