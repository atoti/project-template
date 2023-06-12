from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import timedelta
from functools import lru_cache
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from pydantic import HttpUrl

_Coordinates = tuple[float, float]  # (latitude, longitude)

_COLUMN_NAME_MAPPING: Mapping[str, str] = {
    "result_context": "department",
    "result_city": "city",
    "result_postcode": "postcode",
    "result_street": "street",
    "result_housenumber": "house_number",
}


@lru_cache
def _cached_reverse_geocode(
    stable_coordinates: tuple[_Coordinates, ...],
    /,
    *,
    reverse_geocoding_path: HttpUrl | Path,
    timeout: timedelta,
) -> pd.DataFrame:
    data: StringIO | Path
    coordinates_df = pd.DataFrame(stable_coordinates, columns=["latitude", "longitude"])

    if isinstance(reverse_geocoding_path, Path):
        data = reverse_geocoding_path
    else:
        file = StringIO()
        coordinates_df.to_csv(file, index=False)
        file.seek(0)
        response = requests.post(
            reverse_geocoding_path,
            data=[
                ("result_columns", column_name) for column_name in _COLUMN_NAME_MAPPING
            ],
            files={"data": file},
            timeout=timeout.total_seconds(),
        )
        response.raise_for_status()
        data = StringIO(response.text)

    results_df = pd.read_csv(data)
    assert len(results_df) == len(coordinates_df)
    results_df = results_df.rename(columns=_COLUMN_NAME_MAPPING)

    # Overwrite coordinates with original ones to allow merging this DataFrame with the one of the station information.
    for column_name in coordinates_df.columns:
        results_df[column_name] = coordinates_df[column_name]

    return results_df


def reverse_geocode(
    data: Iterable[_Coordinates],
    /,
    *,
    reverse_geocoding_path: HttpUrl | Path,
    timeout: timedelta,
) -> pd.DataFrame:
    return _cached_reverse_geocode(
        tuple(sorted(data)),
        reverse_geocoding_path=reverse_geocoding_path,
        timeout=timeout,
    )
