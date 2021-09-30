import docker
import requests
import time


def test_docker_container():
    client = docker.from_env()
    client.api.build(".", tag="template")
    container = client.containers.run(
        image="template",
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
