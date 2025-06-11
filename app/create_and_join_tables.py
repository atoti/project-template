import atoti as tt

from .skeleton import Skeleton


def create_station_status_table(skeleton: Skeleton, /) -> None:
    table_skeleton = skeleton.tables.STATION_STATUS
    skeleton.session.create_table(
        table_skeleton.name,
        data_types={
            table_skeleton.STATION_ID.name: tt.LONG,
            table_skeleton.BIKE_TYPE.name: tt.STRING,
            table_skeleton.BIKES.name: tt.INT,
        },
        keys={
            table_skeleton.STATION_ID.name,
            table_skeleton.BIKE_TYPE.name,
        },
    )


def create_station_details_table(skeleton: Skeleton, /) -> None:
    table_skeleton = skeleton.tables.STATION_DETAILS
    skeleton.session.create_table(
        table_skeleton.name,
        data_types={
            table_skeleton.ID.name: tt.LONG,
            table_skeleton.NAME.name: tt.STRING,
            table_skeleton.DEPARTMENT.name: tt.STRING,
            table_skeleton.CITY.name: tt.STRING,
            table_skeleton.POSTCODE.name: tt.INT,
            table_skeleton.STREET.name: tt.STRING,
            table_skeleton.HOUSE_NUMBER.name: tt.STRING,
            table_skeleton.CAPACITY.name: tt.INT,
        },
        default_values={table_skeleton.POSTCODE.name: 0},
        keys={
            table_skeleton.ID.name,
        },
    )


def join_tables(skeleton: Skeleton, /) -> None:
    tables_skeleton = skeleton.tables
    tables_skeleton.STATION_STATUS.table.join(
        tables_skeleton.STATION_DETAILS.table,
        tables_skeleton.STATION_STATUS.STATION_ID.column
        == tables_skeleton.STATION_DETAILS.ID.column,
    )


def create_and_join_tables(skeleton: Skeleton, /) -> None:
    create_station_status_table(skeleton)
    create_station_details_table(skeleton)
    join_tables(skeleton)
