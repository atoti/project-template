from shutil import which
from subprocess import STDOUT, CalledProcessError, check_output
from time import sleep
from typing import Generator, Iterable, Mapping, Optional
from uuid import uuid4

import atoti as tt
import docker
import pytest
from docker.models.containers import Container


def run_command(
    args: Iterable[str], /, *, env: Optional[Mapping[str, str]] = None
) -> str:
    try:
        return check_output(args, env=env, stderr=STDOUT, text=True)
    except CalledProcessError as error:
        raise RuntimeError(f"Command {error.cmd} failed:\n{error.output}") from error


@pytest.fixture(name="docker_bin", scope="session")
def docker_bin_fixture() -> str:
    docker_bin = which("docker")
    assert docker_bin
    return docker_bin


@pytest.fixture(name="docker_image_name", scope="session")
def docker_image_name_fixture(docker_bin: str) -> Generator[str, None, None]:
    name = f"atoti-project-template:{uuid4()}"
    # BuildKit is not supported by Docker's Python SDK.
    # See https://github.com/docker/docker-py/issues/2230.
    build_image_output = run_command(
        [
            docker_bin,
            "build",
            "--tag",
            name,
            ".",
        ],
        env={"DOCKER_BUILDKIT": "1"},
    )
    assert f"naming to docker.io/library/{name}" in build_image_output
    yield name
    remove_image_output = run_command([docker_bin, "image", "rm", name])
    assert "Deleted" in remove_image_output


@pytest.fixture(
    name="docker_container",
    # Don't use this fixture in tests mutating the container or its underlying app.
    scope="session",
)
def docker_container_fixture(
    docker_image_name: str,
) -> Generator[Container, None, None]:
    client = docker.from_env()

    container = client.containers.run(
        docker_image_name,
        detach=True,
        name=str(uuid4()),
        publish_all_ports=True,
    )
    while "Session listening on port" not in str(container.logs()):
        sleep(1)
    yield container
    container.stop()
    container.remove()


@pytest.fixture(name="host_port", scope="session")
def host_port_fixture(docker_bin: str, docker_container: Container) -> int:
    container_port_output = run_command(
        [docker_bin, "container", "port", docker_container.name]
    )
    return int(container_port_output.rsplit(":", maxsplit=1)[-1].strip())


@pytest.fixture(name="query_session_inside_docker_container", scope="session")
def query_session_inside_docker_container_fixture(host_port: int) -> tt.QuerySession:
    return tt.open_query_session(f"http://localhost:{host_port}")
