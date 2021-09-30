import time

import docker
import requests


def test_docker_container():
    client = docker.from_env()
    image, _ = client.images.build(path=".", tag="template")
    container = client.containers.run(
        image=image,
        ports={9090: 9090},
        environment={"ATOTI_DISABLE_TELEMETRY": "true"},
        detach=True,
    )
    while not container.logs():
        time.sleep(1)
    try:
        res = requests.get("http://localhost:9090/versions/rest")
        assert res.status_code == 200
    finally:
        client.api.stop(container.id)
