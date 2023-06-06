from __future__ import annotations

from collections.abc import Iterable, Mapping
from subprocess import STDOUT, CalledProcessError, check_output


def run_command(args: Iterable[str], /, *, env: Mapping[str, str] | None = None) -> str:
    try:
        return check_output(list(args), env=env, stderr=STDOUT, text=True)  # noqa: S603
    except CalledProcessError as error:
        raise RuntimeError(f"Command `{error.cmd}` failed:\n{error.output}") from error
