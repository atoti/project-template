import atoti as tt
import pandas as pd

from app import SKELETON

from .expected_total_capacity import EXPECTED_TOTAL_CAPACITY


def test_total_capacity(session: tt.Session) -> None:
    skeleton = SKELETON.cubes.STATION
    cube = skeleton(session)
    result = cube.query(skeleton.measures.CAPACITY(session))
    expected_result = pd.DataFrame(
        {
            skeleton.measures.CAPACITY.name: pd.Series(
                [EXPECTED_TOTAL_CAPACITY], dtype="Int32"
            ),
        }
    )
    pd.testing.assert_frame_equal(result, expected_result)


def test_departments(session: tt.Session) -> None:
    skeleton = SKELETON.cubes.STATION
    cube = skeleton(session)
    result = cube.query(
        skeleton.measures.CONTRIBUTORS_COUNT(session),
        levels=[
            skeleton.dimensions.STATION_DETAILS.LOCATION.DEPARTMENT(session),
        ],
    )
    assert list(result.index) == [
        "75, Paris, Île-de-France",
        "92, Hauts-de-Seine, Île-de-France",
        "93, Seine-Saint-Denis, Île-de-France",
        "94, Val-de-Marne, Île-de-France",
        "95, Val-d'Oise, Île-de-France",
    ]
