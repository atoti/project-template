import atoti as tt

from .skeleton import SKELETON
from .util.skeleton import column, fact_based_hierarchy


def create_station_cube(session: tt.Session, /) -> None:
    tables = SKELETON.tables
    skeleton = SKELETON.cubes.STATION

    cube = session.create_cube(
        session.tables[tables.STATION_STATUS.key],
        skeleton.name,
        mode="manual",
    )
    h, l, m = cube.hierarchies, cube.levels, cube.measures

    h.update(
        dict(
            [
                fact_based_hierarchy(session, hierarchy)
                for hierarchy in [
                    skeleton.dimensions.STATION_STATUS.hierarchies.BIKE_TYPE,
                    skeleton.dimensions.STATION_DETAILS.hierarchies.LOCATION,
                    skeleton.dimensions.STATION_DETAILS.hierarchies.STATION,
                ]
            ]
        )
    )

    with session.data_model_transaction():
        m[skeleton.measures.BIKES.key] = tt.agg.sum(
            column(session, tables.STATION_STATUS.columns.BIKES)
        )
        m[skeleton.measures.CAPACITY.key] = tt.agg.sum(
            tt.agg.single_value(
                column(session, tables.STATION_DETAILS.columns.CAPACITY)
            ),
            scope=tt.OriginScope(
                {
                    l[
                        skeleton.dimensions.STATION_DETAILS.hierarchies.STATION.levels.ID.key
                    ]
                }
            ),
        )


def create_cubes(session: tt.Session, /) -> None:
    create_station_cube(session)
