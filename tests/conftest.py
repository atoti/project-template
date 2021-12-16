from typing import Generator

import atoti as tt
import pytest

from app import start_session


@pytest.fixture(name="session")
def session_fixture() -> Generator[tt.Session, None, None]:
    with start_session() as session:
        yield session
