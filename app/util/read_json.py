import json
from pathlib import Path
from typing import Any, Union

import requests
from pydantic import HttpUrl


def read_json(base_path: Union[HttpUrl, Path], file_path: Path) -> Any:
    if isinstance(base_path, HttpUrl):
        url = f"{base_path}/{file_path.as_posix()}"
        response = requests.get(url)
        response.raise_for_status()
        body = response.json()
        return body

    data = json.loads((base_path / file_path).read_bytes())
    return data
