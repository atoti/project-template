from typing import Generator

import atoti as tt
import pytest

from app import AppConfig, start_session


@pytest.fixture(name="app_config")
def app_config_fixture() -> AppConfig:
    return AppConfig(
        # user_content_storage=None,
    )


@pytest.fixture(name="session")
def session_fixture(app_config: AppConfig) -> Generator[tt.Session, None, None]:
    with start_session(app_config=app_config) as session:
        yield session
