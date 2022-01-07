from shutil import which
from subprocess import STDOUT, check_output
from time import sleep
from typing import Generator
from uuid import uuid4

import atoti as tt
import docker
import pytest
from docker.models.containers import Container


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
    build_image_output = check_output(
        [docker_bin, "build", "--tag", name, "."],
        env={"DOCKER_BUILDKIT": "1"},
        stderr=STDOUT,
        text=True,
    )
    assert f"naming to docker.io/library/{name}" in build_image_output
    yield name
    remove_image_output = check_output(
        [docker_bin, "image", "rm", name], stderr=STDOUT, text=True
    )
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
    while "Session running" not in str(container.logs()):
        sleep(1)
    yield container
    container.stop()
    container.remove()


@pytest.fixture(name="host_port", scope="session")
def host_port_fixture(docker_bin: str, docker_container: Container) -> int:
    container_port_output = check_output(
        [docker_bin, "container", "port", docker_container.name], text=True
    )
    return int(container_port_output.rsplit(":", maxsplit=1)[-1].strip())


@pytest.fixture(name="query_session_inside_docker_container", scope="session")
def query_session_inside_docker_container_fixture(host_port: int) -> tt.QuerySession:
    return tt.open_query_session(f"http://localhost:{host_port}")
