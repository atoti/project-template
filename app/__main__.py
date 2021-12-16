from . import AppConfig, start_session

app_config = AppConfig()

with start_session(app_config=app_config) as session:
    print(f"Session running at http://localhost:{session.port}")
    session.wait()
