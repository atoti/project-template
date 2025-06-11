import atoti as tt

from .skeleton import SKELETON
from .util import fact_based_hierarchy


def create_station_cube(session: tt.Session, /) -> None:
    tables = SKELETON.tables
    skeleton = SKELETON.cubes.STATION

    cube = session.create_cube(
        SKELETON.tables.STATION_STATUS(session),
        skeleton.name,
        mode="manual",
    )
    h, m = cube.hierarchies, cube.measures

    h.update(
        [
            fact_based_hierarchy(
                session,
                skeleton.dimensions.STATION_DETAILS.LOCATION,
                lambda hierarchy: {
                    hierarchy.DEPARTMENT: tables.STATION_DETAILS.DEPARTMENT,
                    hierarchy.CITY: tables.STATION_DETAILS.CITY,
                    hierarchy.POSTCODE: tables.STATION_DETAILS.POSTCODE,
                    hierarchy.STREET: tables.STATION_DETAILS.STREET,
                    hierarchy.HOUSE_NUMBER: tables.STATION_DETAILS.HOUSE_NUMBER,
                },
            ),
            fact_based_hierarchy(
                session,
                skeleton.dimensions.STATION_DETAILS.STATION,
                lambda hierarchy: {
                    hierarchy.NAME: tables.STATION_DETAILS.NAME,
                    hierarchy.ID: tables.STATION_DETAILS.ID,
                },
            ),
            fact_based_hierarchy(
                session,
                skeleton.dimensions.STATION_STATUS.BIKE_TYPE,
                lambda hierarchy: {
                    hierarchy.BIKE_TYPE: tables.STATION_STATUS.BIKE_TYPE,
                },
            ),
        ]
    )

    with session.data_model_transaction():
        m[skeleton.measures.BIKES.name] = tt.agg.sum(
            tables.STATION_STATUS.BIKES(session)
        )
        m[skeleton.measures.CAPACITY.name] = tt.agg.sum(
            tt.agg.single_value(tables.STATION_DETAILS.CAPACITY(session)),
            scope=tt.OriginScope(
                {skeleton.dimensions.STATION_DETAILS.STATION.ID(session)}
            ),
        )


def create_cubes(session: tt.Session, /) -> None:
    create_station_cube(session)
