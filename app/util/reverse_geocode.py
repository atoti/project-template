from collections.abc import Callable, Iterable, Mapping, Set as AbstractSet
from functools import wraps
from io import BytesIO, StringIO
from pathlib import Path
from typing import Concatenate, ParamSpec

import httpx
import pandas as pd
from pydantic import HttpUrl

_Coordinates = tuple[float, float]  # (latitude, longitude)

_ReverseGeocodedCoordinates = dict[_Coordinates, dict[str, str]]

_COORDINATES_COLUMN_NAMES: Iterable[str] = ["latitude", "longitude"]

_COLUMN_NAME_MAPPING: Mapping[str, str] = {
    "result_context": "department",
    "result_city": "city",
    "result_postcode": "postcode",
    "result_street": "street",
    "result_housenumber": "house_number",
}


_P = ParamSpec("_P")


def _cache(
    function: Callable[
        Concatenate[AbstractSet[_Coordinates], _P], _ReverseGeocodedCoordinates
    ],
    /,
) -> Callable[Concatenate[AbstractSet[_Coordinates], _P], _ReverseGeocodedCoordinates]:
    cache: _ReverseGeocodedCoordinates = {}

    @wraps(function)
    def function_wrapper(
        coordinates: AbstractSet[_Coordinates],
        /,
        *args: _P.args,
        **kwargs: _P.kwargs,
    ) -> _ReverseGeocodedCoordinates:
        uncached_coordinates = coordinates - set(cache)
        result = function(uncached_coordinates, *args, **kwargs)
        cache.update(result)
        return {key: value for key, value in cache.items() if key in coordinates}

    return function_wrapper


@_cache
def _reverse_geocode(
    coordinates: AbstractSet[_Coordinates],
    /,
    *,
    reverse_geocoding_path: HttpUrl | Path,
) -> _ReverseGeocodedCoordinates:
    if not coordinates:
        return {}

    data: StringIO | Path
    coordinates_df = pd.DataFrame(coordinates, columns=list(_COORDINATES_COLUMN_NAMES))

    if isinstance(reverse_geocoding_path, Path):
        data = reverse_geocoding_path
    else:
        file = BytesIO()
        coordinates_df.to_csv(file, index=False)
        file.seek(0)
        response = httpx.post(
            str(reverse_geocoding_path),
            data={"result_columns": list(_COLUMN_NAME_MAPPING)},
            files={"data": file},
        ).raise_for_status()
        data = StringIO(response.text)

    results_df = pd.read_csv(data)
    assert len(results_df) == len(coordinates_df)

    # The returned coordinates are not strictly equal to the input ones.
    # They may have slightly moved.
    # Using input ones to allow the caller to look up the addresses of the coordinates it has.
    for column_name in coordinates_df.columns:
        results_df[column_name] = coordinates_df[column_name]

    results_df = results_df.set_index(list(coordinates_df.columns))
    results_df = results_df.rename(columns=_COLUMN_NAME_MAPPING)
    return results_df.to_dict("index")  # type: ignore[return-value]


def reverse_geocode(
    coordinates: Iterable[_Coordinates],
    /,
    *,
    reverse_geocoding_path: HttpUrl | Path,
) -> pd.DataFrame:
    result = _reverse_geocode(
        set(coordinates), reverse_geocoding_path=reverse_geocoding_path
    )
    result_df = pd.DataFrame.from_dict(result, orient="index")
    index = result_df.index.set_names(_COORDINATES_COLUMN_NAMES)
    result_df.index = index
    return result_df.reset_index()
