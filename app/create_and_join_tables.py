from __future__ import annotations

import atoti as tt

from .constants import StationDetailsTableColumn, StationStatusTableColumn, Table


def create_station_status_table(session: tt.Session, /) -> None:
    session.create_table(
        Table.STATION_STATUS.value,
        keys=[
            StationStatusTableColumn.STATION_ID.value,
            StationStatusTableColumn.BIKE_TYPE.value,
        ],
        types={
            StationStatusTableColumn.STATION_ID.value: tt.LONG,
            StationStatusTableColumn.BIKE_TYPE.value: tt.STRING,
            StationStatusTableColumn.BIKES.value: tt.INT,
        },
    )


def create_station_details_table(session: tt.Session, /) -> None:
    session.create_table(
        Table.STATION_DETAILS.value,
        keys=[
            StationDetailsTableColumn.ID.value,
        ],
        types={
            StationDetailsTableColumn.ID.value: tt.LONG,
            StationDetailsTableColumn.NAME.value: tt.STRING,
            StationDetailsTableColumn.DEPARTMENT.value: tt.STRING,
            StationDetailsTableColumn.CITY.value: tt.STRING,
            StationDetailsTableColumn.POSTCODE.value: tt.INT,
            StationDetailsTableColumn.STREET.value: tt.STRING,
            StationDetailsTableColumn.HOUSE_NUMBER.value: tt.STRING,
            StationDetailsTableColumn.CAPACITY.value: tt.INT,
        },
        default_values={StationDetailsTableColumn.POSTCODE.value: 0},
    )


def join_tables(session: tt.Session, /) -> None:
    session.tables[Table.STATION_STATUS.value].join(
        session.tables[Table.STATION_DETAILS.value],
        session.tables[Table.STATION_STATUS.value][
            StationStatusTableColumn.STATION_ID.value
        ]
        == session.tables[Table.STATION_DETAILS.value][
            StationDetailsTableColumn.ID.value
        ],
    )


def create_and_join_tables(session: tt.Session, /) -> None:
    create_station_status_table(session)
    create_station_details_table(session)
    join_tables(session)
