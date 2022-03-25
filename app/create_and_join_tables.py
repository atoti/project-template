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
            StationStatusTableColumn.STATION_ID.value: tt.type.LONG,
            StationStatusTableColumn.BIKE_TYPE.value: tt.type.STRING,
            StationStatusTableColumn.BIKES.value: tt.type.INT,
        },
    )


def create_station_details_table(session: tt.Session, /) -> None:
    session.create_table(
        Table.STATION_DETAILS.value,
        keys=[
            StationDetailsTableColumn.ID.value,
        ],
        types={
            StationDetailsTableColumn.ID.value: tt.type.LONG,
            StationDetailsTableColumn.NAME.value: tt.type.STRING,
            StationDetailsTableColumn.DEPARTMENT.value: tt.type.STRING,
            StationDetailsTableColumn.CITY.value: tt.type.STRING,
            StationDetailsTableColumn.POSTCODE.value: tt.type.INT,
            StationDetailsTableColumn.STREET.value: tt.type.STRING,
            StationDetailsTableColumn.HOUSE_NUMBER.value: tt.type.STRING,
            StationDetailsTableColumn.CAPACITY.value: tt.type.INT,
        },
    )


def join_tables(session: tt.Session, /) -> None:
    session.tables[Table.STATION_STATUS.value].join(
        session.tables[Table.STATION_DETAILS.value],
        mapping={
            StationStatusTableColumn.STATION_ID.value: StationDetailsTableColumn.ID.value
        },
    )


def create_and_join_tables(session: tt.Session, /) -> None:
    create_station_status_table(session)
    create_station_details_table(session)
    join_tables(session)
