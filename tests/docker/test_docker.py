import atoti as tt

from app import Cube


def test_session_inside_docker_container(
    session_inside_docker_container: tt.Session,
) -> None:
    cube = session_inside_docker_container.cubes[Cube.STATION.value]
    result_df = cube.query(cube.measures["contributors.COUNT"])
    assert result_df["contributors.COUNT"][0] > 0
