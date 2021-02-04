from .start_session import start_session

session = start_session()
print(f"Session running at {session.url}")
session.wait()
