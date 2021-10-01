import subprocess
import time
from http import HTTPStatus

import docker
import requests

IMAGE_TAG = "atoti-template"
SESSION_PORT = 9090


def test_docker_container():
    # Docker buildkit not supported by the Python SDK
    command = ["docker", "build", "--tag", IMAGE_TAG, "."]
    subprocess.run(command, check=True, env={"DOCKER_BUILDKIT": "1"})
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
