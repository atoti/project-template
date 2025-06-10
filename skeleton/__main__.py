from pathlib import Path

from . import SKELETON, generate
from .generate import _SESSION_CONSTANT_NAME

_APP_DIRECTORY = Path(__file__).parent.parent / "app"


def main() -> None:
    code = generate(SKELETON)
    directory = _APP_DIRECTORY / "skeleton2"
    directory.mkdir(exist_ok=True)
    for filename, text in {
        ".gitignore": "*",
        "__init__.py": f"from .{directory.stem} import {_SESSION_CONSTANT_NAME} as {_SESSION_CONSTANT_NAME}",
        f"{directory.stem}.py": code,
    }.items():
        (directory / filename).write_text(text)


main()
