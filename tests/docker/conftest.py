from __future__ import annotations

import re
from collections.abc import Generator
from datetime import timedelta
from shutil import which
from uuid import uuid4

import atoti as tt
import docker
import pytest
from docker.models.containers import Container

from ._docker_container import docker_container as _docker_container
from ._run_command import run_command
from ._timeout import Timeout


@pytest.fixture(name="docker_executable_path", scope="session")
def docker_executable_path_fixture() -> str:
    docker_executable_path = which("docker")
    assert docker_executable_path
    return docker_executable_path


@pytest.fixture(name="poetry_executable_path", scope="session")
def poetry_executable_path_fixture() -> str:
    poetry_executable_path = which("poetry")
    assert poetry_executable_path
    return poetry_executable_path


@pytest.fixture(name="docker_image_name", scope="session")
def docker_image_name_fixture(
    docker_executable_path: str, poetry_executable_path: str, project_name: str
) -> Generator[str, None, None]:
    tag = f"{project_name}:{uuid4()}"
    build_image_output = run_command(
        [poetry_executable_path, "run", "app", "build-docker", tag]
    )
    assert f"naming to docker.io/library/{tag}" in build_image_output
    yield tag
    remove_image_output = run_command([docker_executable_path, "image", "rm", tag])
    assert re.match("(Deleted|Untagged)", remove_image_output)


@pytest.fixture(name="docker_client", scope="session")
def docker_client_fixture() -> docker.DockerClient:
    return docker.from_env()


@pytest.fixture(
    name="docker_container",
    # Don't use this fixture in tests mutating the container or its underlying app.
    scope="session",
)
def docker_container_fixture(
    docker_client: docker.DockerClient,
    docker_image_name: str,
) -> Generator[Container, None, None]:
    timeout = Timeout(timedelta(minutes=1))

    with _docker_container(docker_image_name, client=docker_client) as container:
        logs = container.logs(stream=True)

        while "Session listening on port" not in next(logs).decode():
            if timeout.timed_out:
                raise RuntimeError(f"Session start timed out:\n{container.logs()}")

        yield container


@pytest.fixture(name="host_port", scope="session")
def host_port_fixture(docker_executable_path: str, docker_container: Container) -> int:
    container_port_output = run_command(
        [docker_executable_path, "container", "port", docker_container.name]
    )
    return int(container_port_output.rsplit(":", maxsplit=1)[-1].strip())


@pytest.fixture(name="query_session_inside_docker_container", scope="session")
def query_session_inside_docker_container_fixture(host_port: int) -> tt.QuerySession:
    return tt.QuerySession(f"http://localhost:{host_port}")
