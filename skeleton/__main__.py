from pathlib import Path

from . import SKELETON, generate
from .generate import _SKELETON_CONSTANT_NAME

_APP_DIRECTORY = Path(__file__).parent.parent / "app"


def main() -> None:
    code = generate(SKELETON)
    directory = _APP_DIRECTORY / "skeleton2"
    directory.mkdir(exist_ok=True)
    skeleton_stem = directory.stem
    for filename, text in {
        ".gitignore": "*",
        "__init__.py": f"from .{skeleton_stem} import {_SKELETON_CONSTANT_NAME} as {_SKELETON_CONSTANT_NAME}",
        f"{skeleton_stem}.py": code,
    }.items():
        (directory / filename).write_text(text)


main()
