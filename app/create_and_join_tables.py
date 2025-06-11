import atoti as tt

from .skeleton import Skeleton
from .util import column


def create_station_status_table(session: tt.Session, /) -> None:
    skeleton = Skeleton.tables.STATION_STATUS
    session.create_table(
        skeleton.name,
        data_types={
            skeleton.STATION_ID.name: tt.LONG,
            skeleton.BIKE_TYPE.name: tt.STRING,
            skeleton.BIKES.name: tt.INT,
        },
        keys={
            skeleton.STATION_ID.name,
            skeleton.BIKE_TYPE.name,
        },
    )


def create_station_details_table(session: tt.Session, /) -> None:
    skeleton = Skeleton.tables.STATION_DETAILS
    session.create_table(
        skeleton.name,
        data_types={
            skeleton.ID.name: tt.LONG,
            skeleton.NAME.name: tt.STRING,
            skeleton.DEPARTMENT.name: tt.STRING,
            skeleton.CITY.name: tt.STRING,
            skeleton.POSTCODE.name: tt.INT,
            skeleton.STREET.name: tt.STRING,
            skeleton.HOUSE_NUMBER.name: tt.STRING,
            skeleton.CAPACITY.name: tt.INT,
        },
        default_values={
            skeleton.POSTCODE.name: 0,
        },
        keys={
            skeleton.ID.name,
        },
    )


def join_tables(session: tt.Session, /) -> None:
    skeleton = Skeleton.tables
    session.tables[skeleton.STATION_STATUS.name].join(
        session.tables[skeleton.STATION_DETAILS.name],
        column(session, skeleton.STATION_STATUS.STATION_ID)
        == column(session, skeleton.STATION_DETAILS.ID),
    )


def create_and_join_tables(session: tt.Session, /) -> None:
    create_station_status_table(session)
    create_station_details_table(session)
    join_tables(session)
