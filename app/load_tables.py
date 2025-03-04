import asyncio
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any, cast

import atoti as tt
import httpx
import pandas as pd
from pydantic import HttpUrl

from .config import Config
from .skeleton import SKELETON
from .util import read_json, reverse_geocode


async def read_station_details(
    *,
    http_client: httpx.AsyncClient,
    reverse_geocoding_path: HttpUrl | Path,
    velib_data_base_path: HttpUrl | Path,
) -> pd.DataFrame:
    columns = SKELETON.tables.STATION_DETAILS.columns
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
            "station_id": columns.ID.name,
            "name": columns.NAME.name,
            "capacity": columns.CAPACITY.name,
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
            "department": columns.DEPARTMENT.name,
            "city": columns.CITY.name,
            "postcode": columns.POSTCODE.name,
            "street": columns.STREET.name,
            "house_number": columns.HOUSE_NUMBER.name,
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
    columns = SKELETON.tables.STATION_STATUS.columns
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
                    columns.STATION_ID.name: station_status["station_id"],
                    columns.BIKE_TYPE.name: bike_type,
                    columns.BIKES.name: bikes,
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

    with tt.mapping_lookup(check=__debug__), session.tables.data_transaction():
        await asyncio.gather(
            session.tables[SKELETON.tables.STATION_DETAILS.key].load_async(
                station_details_df
            ),
            session.tables[SKELETON.tables.STATION_STATUS.key].load_async(
                station_status_df
            ),
        )
