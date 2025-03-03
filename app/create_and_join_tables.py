import atoti as tt

from .skeleton import SKELETON
from .util.skeleton import column


def create_station_status_table(session: tt.Session, /) -> None:
    skeleton = SKELETON.tables.STATION_STATUS
    columns = skeleton.columns
    session.create_table(
        skeleton.name,
        data_types={
            columns.STATION_ID.name: tt.LONG,
            columns.BIKE_TYPE.name: tt.STRING,
            columns.BIKES.name: tt.INT,
        },
        keys={
            columns.STATION_ID.name,
            columns.BIKE_TYPE.name,
        },
    )


def create_station_details_table(session: tt.Session, /) -> None:
    skeleton = SKELETON.tables.STATION_DETAILS
    columns = skeleton.columns
    session.create_table(
        skeleton.name,
        data_types={
            columns.ID.name: tt.LONG,
            columns.NAME.name: tt.STRING,
            columns.DEPARTMENT.name: tt.STRING,
            columns.CITY.name: tt.STRING,
            columns.POSTCODE.name: tt.INT,
            columns.STREET.name: tt.STRING,
            columns.HOUSE_NUMBER.name: tt.STRING,
            columns.CAPACITY.name: tt.INT,
        },
        default_values={columns.POSTCODE.name: 0},
        keys={
            columns.ID.name,
        },
    )


def join_tables(session: tt.Session, /) -> None:
    tables = SKELETON.tables
    session.tables[tables.STATION_STATUS.key].join(
        session.tables[tables.STATION_DETAILS.key],
        column(session, tables.STATION_STATUS.columns.STATION_ID)
        == column(session, tables.STATION_DETAILS.columns.ID),
    )


def create_and_join_tables(session: tt.Session, /) -> None:
    create_station_status_table(session)
    create_station_details_table(session)
    join_tables(session)
