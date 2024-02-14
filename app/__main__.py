from __future__ import annotations

from . import Config, start_app

with start_app(config=Config()) as session:
    print(f"Session listening on port {session.port}")  # noqa: T201
    input("Press Enter to stop the application")
