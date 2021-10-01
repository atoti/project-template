import subprocess
import time
from http import HTTPStatus

import docker
import requests

SESSION_PORT = 9090


def test_docker_container():
    # Docker buildkit not supported by the Python SDK
    command = ["docker", "build", "--tag", "template", "."]
    subprocess.run(command, check=True)
    client = docker.from_env()
    try:
        container = client.containers.run(
            image="template",
            ports={SESSION_PORT: SESSION_PORT},
            environment={"ATOTI_DISABLE_TELEMETRY": "true"},
            detach=True,
        )
        while "Session running" not in str(container.logs()):
            time.sleep(1)
        response = requests.get(f"http://localhost:{SESSION_PORT}/versions/rest")
        assert response.status_code == HTTPStatus.OK
    finally:
        client.api.stop(container.id)
