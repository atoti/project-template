import atoti as tt

from .skeleton2 import SKELETON


def create_station_status_table() -> None:
    skeleton = SKELETON.tables.STATION_STATUS
    SKELETON.session.create_table(
        skeleton.key,
        data_types={
            skeleton.STATION_ID.key: tt.LONG,
            skeleton.BIKE_TYPE.key: tt.STRING,
            skeleton.BIKES.key: tt.INT,
        },
        keys={
            skeleton.STATION_ID.key,
            skeleton.BIKE_TYPE.key,
        },
    )


def create_station_details_table() -> None:
    skeleton = SKELETON.tables.STATION_DETAILS
    SKELETON.session.create_table(
        skeleton.key,
        data_types={
            skeleton.ID.key: tt.LONG,
            skeleton.NAME.key: tt.STRING,
            skeleton.DEPARTMENT.key: tt.STRING,
            skeleton.CITY.key: tt.STRING,
            skeleton.POSTCODE.key: tt.INT,
            skeleton.STREET.key: tt.STRING,
            skeleton.HOUSE_NUMBER.key: tt.STRING,
            skeleton.CAPACITY.key: tt.INT,
        },
        default_values={skeleton.POSTCODE.key: 0},
        keys={
            skeleton.ID.key,
        },
    )


def join_tables() -> None:
    tables = SKELETON.tables
    tables.STATION_STATUS.value.join(
        tables.STATION_DETAILS.value,
        tables.STATION_STATUS.STATION_ID.value == tables.STATION_DETAILS.ID.value,
    )


def create_and_join_tables() -> None:
    create_station_status_table()
    create_station_details_table()
    join_tables()
