from subprocess import check_call
from time import sleep
from http import HTTPStatus

import docker
import requests

IMAGE_TAG = "atoti-template"
SESSION_PORT = 9090


def test_docker_container():
    # BuildKit is not supported by Docker's Python SDK.
    # See https://github.com/docker/docker-py/issues/2230.
    check_call(
        ["docker", "build", "--tag", IMAGE_TAG, "."],
        env={"DOCKER_BUILDKIT": "1"},
    )

    client = docker.from_env()

    try:
        container = client.containers.run(
            image=IMAGE_TAG,
            ports={SESSION_PORT: SESSION_PORT},
            detach=True,
        )
        while "Session running" not in str(container.logs()):
            sleep(1)
        response = requests.get(f"http://localhost:{SESSION_PORT}/versions/rest")
        assert response.status_code == HTTPStatus.OK
    finally:
        client.api.stop(container.id)
