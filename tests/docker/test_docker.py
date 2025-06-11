import atoti as tt

from app import Skeleton

from ..expected_total_capacity import EXPECTED_TOTAL_CAPACITY


def test_session_inside_docker_container(
    session_inside_docker_container: tt.Session,
) -> None:
    skeleton = Skeleton.cubes.STATION
    cube = session_inside_docker_container.cubes[skeleton.name]
    m = cube.measures
    result_df = cube.query(m[skeleton.measures.CAPACITY.name])
    total_capacity = result_df[skeleton.measures.CAPACITY.name][0]
    assert total_capacity > EXPECTED_TOTAL_CAPACITY, (
        "The data fetched from the external API should lead to a greater capacity than the one of the local data since new stations have been created since the data was snapshotted."
    )
