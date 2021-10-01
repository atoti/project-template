from subprocess import check_call
import time
from http import HTTPStatus

import docker
import requests

IMAGE_TAG = "atoti-template"
SESSION_PORT = 9090


def test_docker_container():
    check_call(["docker", "build", "--tag", IMAGE_TAG, "."])
    client = docker.from_env()
    try:
        container = client.containers.run(
            image=IMAGE_TAG,
            ports={SESSION_PORT: SESSION_PORT},
            detach=True,
        )
        while "Session running" not in str(container.logs()):
            time.sleep(1)
        response = requests.get(f"http://localhost:{SESSION_PORT}/versions/rest")
        assert response.status_code == HTTPStatus.OK
    finally:
        client.api.stop(container.id)
