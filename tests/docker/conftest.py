from collections.abc import Generator, Mapping, Sequence
from datetime import timedelta
from pathlib import Path
from shutil import which
from subprocess import STDOUT, CalledProcessError, check_output
from uuid import uuid4

import atoti as tt
import docker
import pytest

from ._docker_container import docker_container as _docker_container
from ._timeout import Timeout


def _run_command(
    args: Sequence[str], /, *, env: Mapping[str, str] | None = None
) -> str:
    try:
        return check_output(args, env=env, stderr=STDOUT, text=True)  # noqa: S603
    except CalledProcessError as error:
        raise RuntimeError(f"Command `{error.cmd}` failed:\n{error.output}") from error


@pytest.fixture(name="docker_bin", scope="session")
def docker_bin_fixture() -> Path:
    docker_bin = which("docker")
    assert docker_bin
    return Path(docker_bin)


@pytest.fixture(name="docker_client", scope="session")
def docker_client_fixture() -> docker.DockerClient:
    return docker.from_env()


@pytest.fixture(name="docker_image_name", scope="session")
def docker_image_name_fixture(
    docker_bin: Path, docker_client: docker.DockerClient, project_name: str
) -> Generator[str, None, None]:
    tag = f"{project_name}:{uuid4()}"

    # BuildKit is enabled by default for all users on Docker Desktop.
    # See https://docs.docker.com/build/buildkit/#getting-started.
    is_buildkit_already_enabled = (
        "docker desktop" in _run_command([str(docker_bin), "version"]).lower()
    )

    # BuildKit is not supported by Docker's Python SDK so `docker_client.images.build` cannot be used.
    # See https://github.com/docker/docker-py/issues/2230.
    output = _run_command(
        [str(docker_bin), "build", "--tag", tag, "."],
        env=None if is_buildkit_already_enabled else {"DOCKER_BUILDKIT": "1"},
    )
    assert f"naming to docker.io/library/{tag}" in output
    yield tag
    docker_client.images.remove(tag)


@pytest.fixture(name="session_inside_docker_container", scope="session")
def session_inside_docker_container_fixture(
    docker_client: docker.DockerClient, docker_image_name: str
) -> Generator[tt.Session, None, None]:
    timeout = Timeout(timedelta(minutes=1))

    with _docker_container(docker_image_name, client=docker_client) as container:
        logs = container.logs(stream=True)

        while "Session listening on port" not in next(logs).decode():
            if timeout.timed_out:
                raise RuntimeError(f"Session start timed out:\n{container.logs()}")

        container.reload()  # Refresh `attrs` to get its `HostPort`.
        host_port = int(
            next(iter(container.attrs["NetworkSettings"]["Ports"].values()))[0][
                "HostPort"
            ]
        )
        session = tt.Session.connect(f"http://localhost:{host_port}")
        yield session
