from __future__ import annotations

from collections.abc import Generator
from datetime import timedelta
from shutil import which
from uuid import uuid4

import atoti as tt
import docker
import pytest

from ._docker_container import docker_container as _docker_container
from ._timeout import Timeout


@pytest.fixture(name="docker_client", scope="session")
def docker_client_fixture() -> docker.DockerClient:
    return docker.from_env()


@pytest.fixture(name="poetry_executable_path", scope="session")
def poetry_executable_path_fixture() -> str:
    poetry_executable_path = which("poetry")
    assert poetry_executable_path
    return poetry_executable_path


@pytest.fixture(name="docker_image_name", scope="session")
def docker_image_name_fixture(
    docker_client: docker.DockerClient, project_name: str
) -> Generator[str, None, None]:
    tag = f"{project_name}:{uuid4()}"
    docker_client.images.build(path=".", rm=True, tag=tag)
    yield tag
    docker_client.images.remove(tag)


@pytest.fixture(
    name="query_session_inside_docker_container",
    scope="session",
)
def query_session_inside_docker_container_fixture(
    docker_client: docker.DockerClient, docker_image_name: str
) -> Generator[tt.QuerySession, None, None]:
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
        query_session = tt.QuerySession(f"http://localhost:{host_port}")

        yield query_session
