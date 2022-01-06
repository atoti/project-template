from functools import lru_cache
from io import StringIO
from pathlib import Path
from typing import Iterable, Tuple, Union

import pandas as pd
import requests
from pydantic import HttpUrl

_Coordinates = Tuple[float, float]  # (latitude, longitude)


@lru_cache
def _cached_reverse_geocode(
    stable_coordinates: Tuple[_Coordinates, ...],
    *,
    reverse_geocoding_path: Union[HttpUrl, Path]
) -> pd.DataFrame:
    data: Union[StringIO, Path]

    if isinstance(reverse_geocoding_path, HttpUrl):
        file = StringIO()
        pd.DataFrame(stable_coordinates, columns=["latitude", "longitude"]).to_csv(
            file, index=False
        )
        file.seek(0)
        response = requests.post(reverse_geocoding_path, files={"data": file})
        response.raise_for_status()
        data = StringIO(response.text)
    else:
        # mypy fails to refines the type of `reverse_geocoding_path` to `Path`.
        data = reverse_geocoding_path  # type: ignore[assignment]

    results_df = pd.read_csv(data)
    results_df = results_df.rename(
        columns={
            "result_context": "department",
            "result_city": "city",
            "result_postcode": "postcode",
            "result_name": "street",
            "result_housenumber": "house_number",
        }
    )
    results_df = results_df[
        [
            "latitude",
            "longitude",
            "department",
            "city",
            "postcode",
            "street",
            "house_number",
        ]
    ]
    return results_df


def reverse_geocode(
    data: Iterable[_Coordinates], *, reverse_geocoding_path: Union[HttpUrl, Path]
) -> pd.DataFrame:
    return _cached_reverse_geocode(
        tuple(sorted(data)), reverse_geocoding_path=reverse_geocoding_path
    )
