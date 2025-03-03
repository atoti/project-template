import atoti as tt
import pandas as pd

from app import SKELETON
from app.util.skeleton import CONTRIBUTORS_COUNT


def test_total_capacity(session: tt.Session) -> None:
    cube = session.cubes[SKELETON.cubes.STATION.key]
    result = cube.query(cube.measures[SKELETON.cubes.STATION.measures.CAPACITY.key])
    expected_result = pd.DataFrame(
        columns=[SKELETON.cubes.STATION.measures.CAPACITY.name],
        data=[
            (45_850),
        ],
        dtype="Int32",
    )
    pd.testing.assert_frame_equal(result, expected_result)


def test_departments(session: tt.Session) -> None:
    cube = session.cubes[SKELETON.cubes.STATION.key]
    l, m = cube.levels, cube.measures
    result = cube.query(
        m[CONTRIBUTORS_COUNT],
        levels=[
            l[
                SKELETON.cubes.STATION.dimensions.STATION_DETAILS.hierarchies.LOCATION.levels.DEPARTMENT.key
            ]
        ],
    )
    assert list(result.index) == [
        "75, Paris, Île-de-France",
        "92, Hauts-de-Seine, Île-de-France",
        "93, Seine-Saint-Denis, Île-de-France",
        "94, Val-de-Marne, Île-de-France",
        "95, Val-d'Oise, Île-de-France",
    ]
