from . import start_session

session = start_session()
print(f"Session running at http://localhost:{session.port}")
session.wait()
