from pathlib import Path

from .generate import SKELETON_CLASS_NAME, generate
from .skeleton import SKELETON, Skeleton

_APP_DIRECTORY = Path(__file__).parent.parent / "app"


def main() -> None:
    code = generate(SKELETON, Skeleton)
    directory = _APP_DIRECTORY / "skeleton"
    directory.mkdir(exist_ok=True)
    for filename, text in {
        ".gitignore": "*",
        "__init__.py": f"from .{directory.stem} import {SKELETON_CLASS_NAME} as {SKELETON_CLASS_NAME}",
        f"{directory.stem}.py": code,
    }.items():
        (directory / filename).write_text(text)


main()
