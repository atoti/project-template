import atoti as tt

from .skeleton import Skeleton
from .util import column, fact_based_hierarchy


def create_station_cube(session: tt.Session, /) -> None:
    skeleton = Skeleton.cubes.STATION

    cube = session.create_cube(
        session.tables[Skeleton.tables.STATION_STATUS.name],
        skeleton.name,
        mode="manual",
    )
    h, l, m = cube.hierarchies, cube.levels, cube.measures

    h.update(
        [
            fact_based_hierarchy(
                session,
                skeleton.dimensions.STATION_DETAILS.LOCATION,
                lambda hierarchy: {
                    hierarchy.DEPARTMENT: Skeleton.tables.STATION_DETAILS.DEPARTMENT,
                    hierarchy.CITY: Skeleton.tables.STATION_DETAILS.CITY,
                    hierarchy.POSTCODE: Skeleton.tables.STATION_DETAILS.POSTCODE,
                    hierarchy.STREET: Skeleton.tables.STATION_DETAILS.STREET,
                    hierarchy.HOUSE_NUMBER: Skeleton.tables.STATION_DETAILS.HOUSE_NUMBER,
                },
            ),
            fact_based_hierarchy(
                session,
                skeleton.dimensions.STATION_DETAILS.STATION,
                lambda hierarchy: {
                    hierarchy.NAME: Skeleton.tables.STATION_DETAILS.NAME,
                    hierarchy.ID: Skeleton.tables.STATION_DETAILS.ID,
                },
            ),
            fact_based_hierarchy(
                session,
                skeleton.dimensions.STATION_STATUS.BIKE_TYPE,
                lambda hierarchy: {
                    hierarchy.BIKE_TYPE: Skeleton.tables.STATION_STATUS.BIKE_TYPE,
                },
            ),
        ]
    )

    with session.data_model_transaction():
        m[skeleton.measures.BIKES.name] = tt.agg.sum(
            column(session, Skeleton.tables.STATION_STATUS.BIKES)
        )
        m[skeleton.measures.CAPACITY.name] = tt.agg.sum(
            tt.agg.single_value(
                column(session, Skeleton.tables.STATION_DETAILS.CAPACITY)
            ),
            scope=tt.OriginScope(
                {l[skeleton.dimensions.STATION_DETAILS.STATION.ID.key]}
            ),
        )


def create_cubes(session: tt.Session, /) -> None:
    create_station_cube(session)
