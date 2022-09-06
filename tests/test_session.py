from http import HTTPStatus

import atoti as tt
import pandas as pd
import requests

from app import Config, Cube, StationCubeLocationLevel, StationCubeMeasure


def test_total_capacity(session: tt.Session) -> None:
    station_cube = session.cubes[Cube.STATION.value]
    result = station_cube.query(
        station_cube.measures[StationCubeMeasure.CAPACITY.value]
    )
    expected_result = pd.DataFrame(
        columns=[StationCubeMeasure.CAPACITY.value],
        data=[
            (44_980),
        ],
    )
    pd.testing.assert_frame_equal(result, expected_result)


def test_departments(session: tt.Session) -> None:
    station_cube = session.cubes[Cube.STATION.value]
    result = station_cube.query(
        station_cube.measures["contributors.COUNT"],
        levels=[station_cube.levels[StationCubeLocationLevel.DEPARTMENT.value]],
    )
    assert list(result.index.values) == [
        "75, Paris, Île-de-France",
        "92, Hauts-de-Seine, Île-de-France",
        "93, Seine-Saint-Denis, Île-de-France",
        "94, Val-de-Marne, Île-de-France",
        "95, Val-d'Oise, Île-de-France",
    ]


def test_basic_authentication(config: Config, session: tt.Session) -> None:
    session_url = f"http://localhost:{session.port}"

    assert (
        config.basic_authentication_users
    ), "Expected some basic authentication users to have been configured."

    for username, password in config.basic_authentication_users:
        assert (
            requests.get(
                session_url, timeout=config.requests_timeout.total_seconds()
            ).status_code
            == HTTPStatus.UNAUTHORIZED
        )
        assert (
            requests.get(
                session_url,
                auth=(username, password),
                timeout=config.requests_timeout.total_seconds(),
            ).status_code
            == HTTPStatus.OK
        )
