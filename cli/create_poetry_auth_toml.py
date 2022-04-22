from pathlib import Path
from textwrap import dedent


def create_poetry_auth_toml(
    directory: Path,
    /,
    *,
    atoti_plus_repository_username: str,
    atoti_plus_repository_password: str,
) -> Path:
    path = directory / "auth.toml"
    repository_name = "atoti-plus"
    content = dedent(
        f"""\
        [http-basic]
        [http-basic.{repository_name}]
        username = "{atoti_plus_repository_username}"
        password = "{atoti_plus_repository_password}"
        """
    )
    path.write_text(content, encoding="utf8")
    return path
