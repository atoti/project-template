import os
from http import HTTPStatus
from subprocess import check_call
from time import sleep

import docker
import pytest
import requests

IMAGE_TAG = "atoti-project-template"
SESSION_PORT = 9090


@pytest.fixture(name="docker_image_built", scope="module")
def build_docker_image() -> None:
    # BuildKit is not supported by Docker's Python SDK.
    # See https://github.com/docker/docker-py/issues/2230.
    check_call(
        ["docker", "build", "--tag", IMAGE_TAG, "."],
        env={"DOCKER_BUILDKIT": "1"},
        shell=os.environ.get("CI", "false").lower() != "true",
    )


@pytest.mark.usefixtures("docker_image_built")
def test_docker_container() -> None:
    client = docker.from_env()

    container = client.containers.run(
        detach=True,
        image=IMAGE_TAG,
        ports={SESSION_PORT: SESSION_PORT},
    )

    try:
        while "Session running" not in str(container.logs()):
            sleep(1)
        response = requests.get(f"http://localhost:{SESSION_PORT}/versions/rest")
        assert response.status_code == HTTPStatus.OK
    finally:
        client.api.stop(container.id)
