from datetime import timedelta
from pathlib import Path
from typing import Annotated

from pydantic import (
    AliasChoices,
    DirectoryPath,
    Field,
    FilePath,
    HttpUrl,
    PostgresDsn,
    TypeAdapter,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

from .util import normalize_postgres_dsn_for_atoti_jdbc


class Config(BaseSettings):
    """Hold all the configuration properties of the app, not only the ones related to Atoti.

    See https://pydantic-docs.helpmanual.io/usage/settings/.
    """

    model_config = SettingsConfigDict(frozen=True)

    data_refresh_period: timedelta | None = timedelta(minutes=1)

    # The $PORT environment variable is used by most PaaS to indicate the port the app server should bind to.
    port: int = 9090

    reverse_geocoding_path: HttpUrl | FilePath = TypeAdapter(HttpUrl).validate_python(
        "https://api-adresse.data.gouv.fr/reverse/csv/"
    )

    user_content_storage: Annotated[
        PostgresDsn | Path | None,
        Field(
            # $DATABASE_URL is used by some PaaS such to designate the URL of the app's primary database.
            # For instance: https://devcenter.heroku.com/articles/heroku-postgresql#designating-a-primary-database.
            validation_alias=AliasChoices("user_content_storage", "database_url")
        ),
    ] = Path("content")

    velib_data_base_path: HttpUrl | DirectoryPath = TypeAdapter(
        HttpUrl
    ).validate_python(
        "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole"
    )

    @field_validator("user_content_storage")
    @classmethod
    def normalize_postgres_dsn(cls, value: object) -> object:
        try:
            postgres_dsn: PostgresDsn = TypeAdapter(PostgresDsn).validate_python(value)
            return normalize_postgres_dsn_for_atoti_jdbc(postgres_dsn)
        except ValueError:
            return value
