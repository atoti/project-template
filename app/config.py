# ruff: noqa: UP007
# Pydantic evaluates type annotations at runtime which does not support `|`.

from __future__ import annotations

from datetime import timedelta
from pathlib import Path
from typing import Annotated, Optional, Union

from pydantic import (
    BaseSettings,
    DirectoryPath,
    Field,
    FilePath,
    HttpUrl,
    PostgresDsn,
    parse_obj_as,
    validator,
)

from .util import normalize_postgres_dsn_for_atoti_sql


class Config(BaseSettings):
    """Hold all the configuration properties of the app, not only the ones related to atoti.

    See https://pydantic-docs.helpmanual.io/usage/settings/.
    """

    data_refresh_period: Optional[timedelta] = timedelta(minutes=1)

    # The $PORT environment variable is used by most PaaS to indicate the port the app server should bind to.
    port: int = 9090

    requests_timeout: timedelta = timedelta(seconds=30)

    reverse_geocoding_path: Union[HttpUrl, FilePath] = parse_obj_as(
        HttpUrl, "https://api-adresse.data.gouv.fr/reverse/csv/"
    )

    user_content_storage: Annotated[
        Optional[Union[PostgresDsn, Path]],
        Field(
            # $DATABASE_URL is used by some PaaS such to designate the URL of the app's primary database.
            # For instance: https://devcenter.heroku.com/articles/heroku-postgresql#designating-a-primary-database.
            env="database_url",
        ),
    ] = Path("content")

    velib_data_base_path: Union[HttpUrl, DirectoryPath] = parse_obj_as(
        HttpUrl,
        "https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole",
    )

    @validator("user_content_storage")
    @classmethod
    def normalize_postgresql_dsn(cls, value: PostgresDsn | object) -> object:
        return (
            normalize_postgres_dsn_for_atoti_sql(value)
            if isinstance(value, PostgresDsn)
            else value
        )

    class Config:
        allow_mutation = False
