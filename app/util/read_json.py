import json
from pathlib import Path

import httpx
from pydantic import HttpUrl


def read_json(base_path: HttpUrl | Path, file_path: Path, /) -> object:
    if isinstance(base_path, Path):
        return json.loads((base_path / file_path).read_bytes())

    url = f"{base_path}/{file_path.as_posix()}"
    response = httpx.get(url).raise_for_status()
    return response.json()
