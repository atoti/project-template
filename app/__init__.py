try:
    from .skeleton import Skeleton as Skeleton
except ImportError as error:
    if __debug__:
        from skeleton import main as _generate_skeleton

        _generate_skeleton()

        from .skeleton import Skeleton as Skeleton
    else:
        message = "The skeleton must be generated before running in production."
        raise RuntimeError(message) from error

from .config import Config as Config
from .start_app import start_app as start_app
