import atoti as tt
import pandas as pd

from app import Cube, StationCubeLocationLevel, StationCubeMeasure


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
