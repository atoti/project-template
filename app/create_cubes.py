import atoti as tt

from .constants import (
    Cube,
    StationCubeBikeTypeLevel,
    StationCubeHierarchy,
    StationCubeLocationLevel,
    StationCubeMeasure,
    StationCubeStationLevel,
    StationDetailsTableColumn,
    StationStatusTableColumn,
    Table,
)


def create_station_cube(session: tt.Session, /) -> None:
    station_details_table = session.tables[Table.STATION_DETAILS.value]
    station_status_table = session.tables[Table.STATION_STATUS.value]

    cube = session.create_cube(station_status_table, Cube.STATION.value, mode="manual")
    h, l, m = cube.hierarchies, cube.levels, cube.measures

    h.update(
        {
            StationCubeHierarchy.BIKE_TYPE.value: {
                StationCubeBikeTypeLevel.BIKE_TYPE.value: station_status_table[
                    StationStatusTableColumn.BIKE_TYPE.value
                ]
            },
            StationCubeHierarchy.LOCATION.value: {
                StationCubeLocationLevel.DEPARTMENT.value: station_details_table[
                    StationDetailsTableColumn.DEPARTMENT.value
                ],
                StationCubeLocationLevel.CITY.value: station_details_table[
                    StationDetailsTableColumn.CITY.value
                ],
                StationCubeLocationLevel.POSTCODE.value: station_details_table[
                    StationDetailsTableColumn.POSTCODE.value
                ],
                StationCubeLocationLevel.STREET.value: station_details_table[
                    StationDetailsTableColumn.STREET.value
                ],
                StationCubeLocationLevel.HOUSE_NUMBER.value: station_details_table[
                    StationDetailsTableColumn.HOUSE_NUMBER.value
                ],
            },
            StationCubeHierarchy.STATION.value: {
                StationCubeStationLevel.NAME.value: station_details_table[
                    StationDetailsTableColumn.NAME.value
                ],
                StationCubeStationLevel.ID.value: station_status_table[
                    StationStatusTableColumn.STATION_ID.value
                ],
            },
        }
    )

    m.update(
        {
            StationCubeMeasure.BIKES.value: tt.agg.sum(
                station_status_table[StationStatusTableColumn.BIKES.value]
            ),
            StationCubeMeasure.CAPACITY.value: tt.agg.sum(
                tt.value(
                    station_details_table[StationDetailsTableColumn.CAPACITY.value]
                ),
                scope=tt.scope.origin(l[StationCubeStationLevel.ID.value]),
            ),
        }
    )


def create_cubes(session: tt.Session, /) -> None:
    create_station_cube(session)
