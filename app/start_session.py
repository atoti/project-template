import os
import re
from typing import Mapping

import atoti as tt
import pandas as pd

POSTGRES_DATABASE_URL_PATTERN = (
    r"(?P<database>postgres://)(?P<username>.*):(?P<password>.*)@(?P<url>.*)"
)


def _get_user_content_storage_config() -> Mapping[str, Mapping[str, str]]:
    database_url = os.environ.get("DATABASE_URL")
    if database_url is None:
        return {}
    match = re.match(POSTGRES_DATABASE_URL_PATTERN, database_url)
    if match is None:
        raise ValueError("Failed to parse database URL")
    username = match.group("username")
    password = match.group("password")
    url = match.group("url")
    if not "postgres" in match.group("database"):
        raise ValueError(f"Expected Postgres database, got {match.group('database')}")
    return {
        "user_content_storage": {
            "url": f"postgresql://{url}?user={username}&password={password}"
        }
    }


def start_session() -> tt.Session:
    session = tt.create_session(
        config={
            **{
                "java_options": ["-Xmx250m"],
                # The $PORT environment variable is used by most PaaS to indicate the port the application server should bind to.
                "port": int(os.environ.get("PORT") or 9090),
            },
            **_get_user_content_storage_config(),
        }
    )
    table = session.read_pandas(
        pd.DataFrame(
            columns=["Product", "Price"],
            data=[
                ("car", 20000.0),
                ("computer", 1000.0),
                ("phone", 500.0),
                ("game", 60.0),
            ],
        ),
        table_name="Products",
    )
    session.create_cube(table)
    return session
