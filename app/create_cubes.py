import atoti as tt

from .skeleton import SKELETON
from .util.skeleton import column


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
        {
            skeleton.dimensions.STATION_STATUS.hierarchies.BIKE_TYPE.key: {
                skeleton.dimensions.STATION_STATUS.hierarchies.BIKE_TYPE.levels.BIKE_TYPE.name: column(
                    session, tables.STATION_STATUS.columns.BIKE_TYPE
                )
            },
            skeleton.dimensions.STATION_DETAILS.hierarchies.LOCATION.key: {
                skeleton.dimensions.STATION_DETAILS.hierarchies.LOCATION.levels.DEPARTMENT.name: column(
                    session, tables.STATION_DETAILS.columns.DEPARTMENT
                ),
                skeleton.dimensions.STATION_DETAILS.hierarchies.LOCATION.levels.CITY.name: column(
                    session, tables.STATION_DETAILS.columns.CITY
                ),
                skeleton.dimensions.STATION_DETAILS.hierarchies.LOCATION.levels.POSTCODE.name: column(
                    session, tables.STATION_DETAILS.columns.POSTCODE
                ),
                skeleton.dimensions.STATION_DETAILS.hierarchies.LOCATION.levels.STREET.name: column(
                    session, tables.STATION_DETAILS.columns.STREET
                ),
                skeleton.dimensions.STATION_DETAILS.hierarchies.LOCATION.levels.HOUSE_NUMBER.name: column(
                    session, tables.STATION_DETAILS.columns.HOUSE_NUMBER
                ),
            },
            skeleton.dimensions.STATION_DETAILS.hierarchies.STATION.key: {
                skeleton.dimensions.STATION_DETAILS.hierarchies.STATION.levels.NAME.name: column(
                    session, tables.STATION_DETAILS.columns.NAME
                ),
                skeleton.dimensions.STATION_DETAILS.hierarchies.STATION.levels.ID.name: column(
                    session, tables.STATION_STATUS.columns.STATION_ID
                ),
            },
        }
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
