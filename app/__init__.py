try:
    from .skeleton import Skeleton as Skeleton
except ImportError:
    message = "Generate the skeleton with `uv run -m skeleton` and retry."
    raise RuntimeError(message) from None

from .config import Config as Config
from .start_app import start_app as start_app
