from pathlib import Path

from . import SKELETON, generate

_APP_DIRECTORY = Path(__file__).parent.parent / "app"


def main() -> None:
    code = generate(SKELETON)
    (_APP_DIRECTORY / "skeleton2.py").write_text(code)


main()
