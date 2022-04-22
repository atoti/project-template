import typer

from .get_executable_path import get_executable_path
from .run_command import run_command

app = typer.Typer()


_APP_PACKAGE = "app"
_PACKAGES = (_APP_PACKAGE, "cli", "tests")

_CHECK_OPTION = typer.Option(False, "--check/--fix")


@app.command(help="Build the Docker image.")
def build_docker(tag: str) -> None:
    run_command(
        [get_executable_path("docker"), "build", "--tag", tag, "."],
        env={"DOCKER_BUILDKIT": "1"},
    )


@app.command(help="Format the project files.")
def format(check: bool = _CHECK_OPTION) -> None:  # pylint: disable=redefined-builtin
    run_command(
        ["black"] + (["--check"] if check else []) + ["."], run_with_poetry=True
    )


@app.command(help="Lint the project files.")
def lint() -> None:
    run_command(["pylint", "--jobs=0", *_PACKAGES], run_with_poetry=True)


@app.command(help="Sort imports in Python files.")
def sort_imports(check: bool = _CHECK_OPTION) -> None:
    run_command(
        ["isort"] + (["--check"] if check else []) + ["--gitignore", "."],
        run_with_poetry=True,
    )


@app.command(help="Start the app.")
def start() -> None:
    run_command(["python", "-u", "-m", _APP_PACKAGE], run_with_poetry=True)


@app.command(help="Run the test suite.")
def test() -> None:
    run_command(["pytest", "--numprocesses", "auto"], run_with_poetry=True)


@app.command(help="Statically check the Python types.")
def typecheck() -> None:
    run_command(
        [
            "mypy",
            "--show-error-codes",
            *[arg for package in _PACKAGES for arg in ["--package", package]],
        ],
        run_with_poetry=True,
    )
