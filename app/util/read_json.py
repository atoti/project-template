import json
from datetime import timedelta
from pathlib import Path
from typing import Any, Union

import requests
from pydantic import HttpUrl


def read_json(
    base_path: Union[HttpUrl, Path], file_path: Path, /, *, timeout: timedelta
) -> Any:
    if isinstance(base_path, HttpUrl):
        url = f"{base_path}/{file_path.as_posix()}"
        response = requests.get(url, timeout=timeout.total_seconds())
        response.raise_for_status()
        body = response.json()
        return body

    data = json.loads((base_path / file_path).read_bytes())
    return data
