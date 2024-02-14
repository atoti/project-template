from __future__ import annotations

from collections.abc import Generator
from pathlib import Path

import atoti as tt
import pytest

from app import Config, start_app

_TESTS_DIRECTORY = Path(__file__).parent
_TESTS_DATA_PATH = _TESTS_DIRECTORY / "data"
_PROJECT_DIRECTORY = _TESTS_DIRECTORY.parent


@pytest.fixture(name="project_name", scope="session")
def project_name_fixture() -> str:
    return _PROJECT_DIRECTORY.name


@pytest.fixture(name="config", scope="session")
def config_fixture() -> Config:
    return Config(
        data_refresh_period=None,
        reverse_geocoding_path=_TESTS_DATA_PATH / "station_location.csv",
        port=0,
        user_content_storage=None,
        velib_data_base_path=_TESTS_DATA_PATH,
    )


@pytest.fixture(
    name="session",
    # Don't use this fixture in tests mutating the app or its underlying session.
    scope="session",
)
def session_fixture(config: Config) -> Generator[tt.Session, None, None]:
    with start_app(config=config) as session:
        yield session
