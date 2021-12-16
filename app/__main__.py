from . import start_session

with start_session() as session:
    print(f"Session running at http://localhost:{session.port}")
    session.wait()
