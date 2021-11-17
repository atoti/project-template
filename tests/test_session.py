import pandas as pd
from pandas._testing import assert_frame_equal

from app import start_session


def test_price_sum() -> None:
    session = start_session()
    cube = session.cubes["Products"]
    actual_result = cube.query(cube.measures["Price.SUM"])
    expected_result = pd.DataFrame(
        columns=["Price.SUM"],
        data=[
            (21560.00),
        ],
    )
    assert_frame_equal(actual_result, expected_result)
