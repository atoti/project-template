from shlex import join
from subprocess import run
from typing import Mapping, Optional, Sequence

import typer

from .get_executable_path import get_executable_path


def run_command(
    command: Sequence[str],
    /,
    *,
    env: Optional[Mapping[str, str]] = None,
    run_with_poetry: bool = False,
) -> None:
    if run_with_poetry:
        command = [get_executable_path("poetry"), "run"] + list(command)

    typer.echo(f"$ {join(command)}", err=True)
    run(command, check=True, env=env)
