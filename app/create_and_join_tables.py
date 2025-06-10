import atoti as tt

from .skeleton2 import SESSION


def create_station_status_table() -> None:
    table = SESSION.tables.STATION_STATUS
    SESSION.value.create_table(
        table.key,
        data_types={
            table.STATION_ID.key: tt.LONG,
            table.BIKE_TYPE.key: tt.STRING,
            table.BIKES.key: tt.INT,
        },
        keys={
            table.STATION_ID.key,
            table.BIKE_TYPE.key,
        },
    )


def create_station_details_table() -> None:
    table = SESSION.tables.STATION_DETAILS
    SESSION.value.create_table(
        table.key,
        data_types={
            table.ID.key: tt.LONG,
            table.NAME.key: tt.STRING,
            table.DEPARTMENT.key: tt.STRING,
            table.CITY.key: tt.STRING,
            table.POSTCODE.key: tt.INT,
            table.STREET.key: tt.STRING,
            table.HOUSE_NUMBER.key: tt.STRING,
            table.CAPACITY.key: tt.INT,
        },
        default_values={table.POSTCODE.key: 0},
        keys={
            table.ID.key,
        },
    )


def join_tables() -> None:
    tables = SESSION.tables
    tables.STATION_STATUS.value.join(
        tables.STATION_DETAILS.value,
        tables.STATION_STATUS.STATION_ID.value == tables.STATION_DETAILS.ID.value,
    )


def create_and_join_tables() -> None:
    create_station_status_table()
    create_station_details_table()
    join_tables()
