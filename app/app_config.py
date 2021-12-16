from pathlib import Path
from typing import Any, List, Optional, Union
from urllib.parse import urlencode, urlparse

from pydantic import BaseSettings, Field, PostgresDsn, validator


def normalize_postgresql_dsn_for_atoti_sql(url: PostgresDsn) -> Any:
    parts = urlparse(url)

    query_parts: List[str] = []

    if parts.query:
        query_parts.append(parts.query)

    if parts.username or parts.password:
        query_parts.append(
            urlencode({"user": parts.username, "password": parts.password})
        )

    return PostgresDsn(
        # This is how pydantic creates an instance from parts.
        None,
        scheme="postgresql",
        host=str(parts.hostname),
        port=str(parts.port) if parts.port else None,
        path=parts.path,
        query="&".join(query_parts) if query_parts else None,
        fragment=parts.fragment,
    )


class AppConfig(BaseSettings):
    """Hold all the configuration properties of the app, not only the ones related to atoti."""

    # The $PORT environment variable is used by most PaaS to indicate the port the app server should bind to.
    port: int = 9090

    user_content_storage: Optional[Union[PostgresDsn, Path]] = Field(
        default=Path("content"),
        # $DATABASE_URL is used by some PaaS such to designate the URL of the app's primary database.
        # For instance: https://devcenter.heroku.com/articles/heroku-postgresql#designating-a-primary-database.
        env="database_url",
    )

    @validator("user_content_storage")
    @classmethod
    def normalize_postgresql_dsn(cls, value: Union[PostgresDsn, Any]) -> Any:
        return (
            normalize_postgresql_dsn_for_atoti_sql(value)
            if isinstance(value, PostgresDsn)
            else value
        )
