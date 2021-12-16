import sys
from typing import Any, Dict

import atoti as tt
import pandas as pd
from pydantic import AnyUrl

from .app_config import AppConfig


def create_session(*, app_config: AppConfig) -> tt.Session:
    session_config: Dict[str, Any] = {
        "logging": {"destination": sys.stdout},
        "port": app_config.port,
    }

    if app_config.user_content_storage:
        session_config["user_content_storage"] = (
            {"url": str(app_config.user_content_storage)}
            if isinstance(app_config.user_content_storage, AnyUrl)
            else app_config.user_content_storage
        )

    return tt.create_session(config=session_config)


def start_session(*, app_config: AppConfig) -> tt.Session:
    session = create_session(app_config=app_config)
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
