from pathlib import Path
from typing import Generator

import atoti as tt
import pytest

from app import App, Config

TEST_DATA_PATH = Path(__file__).parent / "data"


@pytest.fixture(name="config", scope="session")
def config_fixture() -> Config:
    return Config(
        data_refresh_period=None,
        reverse_geocoding_path=TEST_DATA_PATH / "station_location.csv",
        port=0,
        user_content_storage=None,
        velib_data_base_path=TEST_DATA_PATH,
    )


@pytest.fixture(
    name="app",
    # Don't use this fixture in tests mutating the app or its underlying session.
    scope="session",
)
def app_fixture(config: Config) -> Generator[App, None, None]:
    with App(config=config) as app:
        yield app


@pytest.fixture(name="session", scope="session")
def session_fixture(app: App) -> tt.Session:
    return app.session
