import atoti as tt

from app import SKELETON
from app.util.skeleton import CONTRIBUTORS_COUNT


def test_session_inside_docker_container(
    session_inside_docker_container: tt.Session,
) -> None:
    cube = session_inside_docker_container.cubes[SKELETON.cubes.STATION.key]
    result_df = cube.query(cube.measures[CONTRIBUTORS_COUNT])
    assert result_df[CONTRIBUTORS_COUNT][0] > 0
