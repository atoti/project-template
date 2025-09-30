import os

import pytest

# Doing this before any import of `atoti`.
# Setting the variable using `os.environ` instead of pytest's `MonkeyPatch` so that the change happens before pytest evaluates other modules.
os.environ["ATOTI_HIDE_EULA_MESSAGE"] = str(True)


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    return "asyncio"
