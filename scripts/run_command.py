from shlex import join
from sys import argv
from subprocess import run
from typing import Iterable


def run_command(
    *args: str, check_args: Iterable[str] = (), fix_args: Iterable[str] = ()
) -> None:
    command = [
        *args,
        *(fix_args if "--fix" in argv else check_args),
    ]
    print(f"$ {join(command)}")
    run(
        command,
        check=True,
    )
