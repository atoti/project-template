from collections.abc import Mapping, Sequence
from subprocess import STDOUT, CalledProcessError, check_output


def run_command(args: Sequence[str], /, *, env: Mapping[str, str] | None = None) -> str:
    try:
        return check_output(args, env=env, stderr=STDOUT, text=True)  # noqa: S603
    except CalledProcessError as error:
        raise RuntimeError(f"Command `{error.cmd}` failed:\n{error.output}") from error
