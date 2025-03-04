import atoti as tt

from app import SKELETON

from ..total_capacity import TOTAL_CAPACITY


def test_session_inside_docker_container(
    session_inside_docker_container: tt.Session,
) -> None:
    skeleton = SKELETON.cubes.STATION
    cube = session_inside_docker_container.cubes[skeleton.key]
    result_df = cube.query(cube.measures[skeleton.measures.CAPACITY.key])
    total_capacity = result_df[skeleton.measures.CAPACITY.name][0]
    assert total_capacity > 0, (
        "There should be at least one station with one dock or more."
    )
    assert total_capacity != TOTAL_CAPACITY, (
        "The data fetched from the external API should lead to a different capacity than the one of the local data since new stations have been created since the data was snapshotted."
    )
