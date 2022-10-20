import atoti as tt
import pytest

from app import Cube


@pytest.mark.skip
def test_query_session_inside_docker_container(
    query_session_inside_docker_container: tt.QuerySession,
) -> None:
    cube = query_session_inside_docker_container.cubes[Cube.STATION.value]
    result_df = cube.query(cube.measures["contributors.COUNT"])
    assert result_df["contributors.COUNT"][0] > 0
