import json
from pathlib import Path

import httpx
from pydantic import HttpUrl


async def read_json(
    base_path: HttpUrl | Path,
    file_path: Path,
    /,
    *,
    http_client: httpx.AsyncClient,
) -> object:
    if isinstance(base_path, Path):
        return json.loads((base_path / file_path).read_bytes())

    url = f"{base_path}/{file_path.as_posix()}"
    response = await http_client.get(url)
    return response.raise_for_status().json()
