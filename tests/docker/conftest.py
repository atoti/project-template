import re
from datetime import timedelta
from shutil import which
from subprocess import STDOUT, CalledProcessError, check_output
from time import sleep
from typing import Generator, Iterable, Mapping, Optional
from uuid import uuid4

import atoti as tt
import docker
import pytest
from docker.models.containers import Container

from .timeout import Timeout


def run_command(
    args: Iterable[str], /, *, env: Optional[Mapping[str, str]] = None
) -> str:
    try:
        return check_output(list(args), env=env, stderr=STDOUT, text=True)
    except CalledProcessError as error:
        raise RuntimeError(f"Command {error.cmd} failed:\n{error.output}") from error


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
    docker_executable_path: str, poetry_executable_path: str
) -> Generator[str, None, None]:
    tag = f"atoti-project:{uuid4()}"
    build_image_output = run_command(
        [poetry_executable_path, "run", "app", "build-docker", tag]
    )
    assert f"naming to docker.io/library/{tag}" in build_image_output
    yield tag
    remove_image_output = run_command([docker_executable_path, "image", "rm", tag])
    assert re.match("(Deleted|Untagged)", remove_image_output)


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

    try:
        timeout = Timeout(timedelta(minutes=1))
        while "Session listening on port" not in str(container.logs()):
            if timeout.timed_out:
                raise RuntimeError(f"Session start timed out:\n{container.logs()}")
            sleep(1)
        yield container
    finally:
        container.stop()
        container.remove()


@pytest.fixture(name="host_port", scope="session")
def host_port_fixture(docker_executable_path: str, docker_container: Container) -> int:
    container_port_output = run_command(
        [docker_executable_path, "container", "port", docker_container.name]
    )
    return int(container_port_output.rsplit(":", maxsplit=1)[-1].strip())


@pytest.fixture(name="query_session_inside_docker_container", scope="session")
def query_session_inside_docker_container_fixture(host_port: int) -> tt.QuerySession:
    return tt.open_query_session(f"http://localhost:{host_port}")
