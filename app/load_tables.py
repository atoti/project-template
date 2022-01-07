from pathlib import Path
from typing import Any, List, Mapping, Tuple, Union, cast

import atoti as tt
import pandas as pd
from pydantic import HttpUrl

from .config import Config
from .constants import StationDetailsTableColumn, StationStatusTableColumn, Table
from .util import read_json, reverse_geocode


def read_station_details(
    *,
    reverse_geocoding_path: Union[HttpUrl, Path],
    velib_data_base_path: Union[HttpUrl, Path],
) -> pd.DataFrame:
    stations_data = read_json(velib_data_base_path, Path("station_information.json"))[
        "data"
    ]["stations"]
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

    # Drop some precision to ensure stability of reverse geocoding results.
    station_information_df = station_information_df.round(
        {"latitude": 6, "longitude": 6}
    )

    coordinates = cast(
        List[Tuple[float, float]],
        station_information_df[["latitude", "longitude"]].itertuples(
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
        reverse_geocoded_df, how="left", on=["latitude", "longitude"]
    ).drop(columns=["latitude", "longitude"])


def read_station_status(velib_data_base_path: Union[HttpUrl, Path], /) -> pd.DataFrame:
    stations_data = read_json(velib_data_base_path, Path("station_status.json"))[
        "data"
    ]["stations"]
    station_statuses: List[Mapping[str, Any]] = []
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
    station_statuses_df = pd.DataFrame(station_statuses)
    return station_statuses_df


def load_tables(session: tt.Session, /, *, config: Config) -> None:
    station_details_df = read_station_details(
        reverse_geocoding_path=config.reverse_geocoding_path,
        velib_data_base_path=config.velib_data_base_path,
    )
    station_status_df = read_station_status(config.velib_data_base_path)

    with session.start_transaction():
        session.tables[Table.STATION_DETAILS.value].load_pandas(station_details_df)
        session.tables[Table.STATION_STATUS.value].load_pandas(station_status_df)
