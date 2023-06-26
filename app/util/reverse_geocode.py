from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import timedelta
from functools import wraps
from io import StringIO
from pathlib import Path
from typing import AbstractSet, Any, Callable, TypeVar, cast

import pandas as pd
import requests
from pydantic import HttpUrl
from typing_extensions import ParamSpec

_Coordinates = tuple[float, float]  # (latitude, longitude)

_COORDINATES_COLUMN_NAMES: Iterable[str] = ["latitude", "longitude"]

_COLUMN_NAME_MAPPING: Mapping[str, str] = {
    "result_context": "department",
    "result_city": "city",
    "result_postcode": "postcode",
    "result_street": "street",
    "result_housenumber": "house_number",
}

_P = ParamSpec("_P")
_R = TypeVar("_R")


def _cache(function: Callable[_P, _R], /) -> Callable[_P, _R]:
    cache: dict[_Coordinates, dict[str, str]] = {}

    @wraps(function)
    def function_wrapper(
        *args: _P.args,
        **kwargs: _P.kwargs,
    ) -> _R:
        coordinates, *tail = args
        assert isinstance(coordinates, AbstractSet)
        new_coordinates = coordinates - set(cache)
        new_args = cast(_P.args, (new_coordinates, *tail))
        result = function(*new_args, **kwargs)
        cache.update(cast(Any, result))
        return result

    return function_wrapper


@_cache
def _reverse_geocode(
    coordinates: AbstractSet[_Coordinates],
    /,
    *,
    reverse_geocoding_path: HttpUrl | Path,
    timeout: timedelta,
) -> dict[_Coordinates, dict[str, str]]:
    if not coordinates:
        return {}

    data: StringIO | Path
    coordinates_df = pd.DataFrame(coordinates, columns=list(_COORDINATES_COLUMN_NAMES))

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
    timeout: timedelta,
) -> pd.DataFrame:
    result = _reverse_geocode(
        set(coordinates), reverse_geocoding_path=reverse_geocoding_path, timeout=timeout
    )
    result_df = pd.DataFrame.from_dict(result, orient="index")
    index = result_df.index.set_names(_COORDINATES_COLUMN_NAMES)
    result_df.index = index
    return result_df.reset_index()
