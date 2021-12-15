from typing import Generator

import atoti as tt
import pandas as pd
import pytest
from pandas._testing import assert_frame_equal

from app import start_session


@pytest.fixture(name="session")
def session_fixture() -> Generator[tt.Session, None, None]:
    with start_session() as session:
        yield session


def test_price_sum(session: tt.Session) -> None:
    cube = session.cubes["Products"]
    actual_result = cube.query(cube.measures["Price.SUM"])
    expected_result = pd.DataFrame(
        columns=["Price.SUM"],
        data=[
            (21560.00),
        ],
    )
    assert_frame_equal(actual_result, expected_result)
