import asyncio
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, cast

import atoti as tt
import httpx
import pandas as pd
from pydantic import HttpUrl

from .config import Config
from .constants import StationDetailsTableColumn, StationStatusTableColumn, Table
from .util import read_json, reverse_geocode


async def read_station_details(
    *,
    http_client: httpx.AsyncClient,
    reverse_geocoding_path: HttpUrl | Path,
    velib_data_base_path: HttpUrl | Path,
) -> pd.DataFrame:
    stations_data: Any = cast(
        Any,
        await read_json(
            velib_data_base_path,
            Path("station_information.json"),
            http_client=http_client,
        ),
    )["data"]["stations"]
    station_information_df = pd.DataFrame(stations_data)[
        ["station_id", "name", "capacity", "lat", "lon"]
    ].rename(
        columns={
            "station_id": StationDetailsTableColumn.ID.value,
            "name": StationDetailsTableColumn.NAME.value,
            "capacity": StationDetailsTableColumn.CAPACITY.value,
            "lat": "latitude",
            "lon": "longitude",
        }
    )

    coordinates_column_names = ["latitude", "longitude"]

    coordinates = cast(
        Iterable[tuple[float, float]],
        station_information_df[coordinates_column_names].itertuples(
            index=False, name=None
        ),
    )

    reverse_geocoded_df = reverse_geocode(
        coordinates, reverse_geocoding_path=reverse_geocoding_path
    ).rename(
        columns={
            "department": StationDetailsTableColumn.DEPARTMENT.value,
            "city": StationDetailsTableColumn.CITY.value,
            "postcode": StationDetailsTableColumn.POSTCODE.value,
            "street": StationDetailsTableColumn.STREET.value,
            "house_number": StationDetailsTableColumn.HOUSE_NUMBER.value,
        }
    )

    return station_information_df.merge(
        reverse_geocoded_df, how="left", on=coordinates_column_names
    ).drop(columns=coordinates_column_names)


async def read_station_status(
    velib_data_base_path: HttpUrl | Path,
    /,
    *,
    http_client: httpx.AsyncClient,
) -> pd.DataFrame:
    stations_data = cast(
        Any,
        await read_json(
            velib_data_base_path,
            Path("station_status.json"),
            http_client=http_client,
        ),
    )["data"]["stations"]
    station_statuses: list[Mapping[str, Any]] = []
    for station_status in stations_data:
        for num_bikes_available_types in station_status["num_bikes_available_types"]:
            if len(num_bikes_available_types) != 1:
                raise ValueError(
                    f"Expected a single bike type but found: {list(num_bikes_available_types.keys())}"
                )
            bike_type, bikes = next(iter(num_bikes_available_types.items()))
            station_statuses.append(
                {
                    StationStatusTableColumn.STATION_ID.value: station_status[
                        "station_id"
                    ],
                    StationStatusTableColumn.BIKE_TYPE.value: bike_type,
                    StationStatusTableColumn.BIKES.value: bikes,
                }
            )
    return pd.DataFrame(station_statuses)


async def load_tables(
    session: tt.Session,
    /,
    *,
    config: Config,
    http_client: httpx.AsyncClient,
) -> None:
    station_details_df, station_status_df = await asyncio.gather(
        read_station_details(
            http_client=http_client,
            reverse_geocoding_path=config.reverse_geocoding_path,
            velib_data_base_path=config.velib_data_base_path,
        ),
        read_station_status(
            config.velib_data_base_path,
            http_client=http_client,
        ),
    )

    with session.tables.data_transaction():
        await asyncio.gather(
            session.tables[Table.STATION_DETAILS.value].load_async(station_details_df),
            session.tables[Table.STATION_STATUS.value].load_async(station_status_df),
        )
