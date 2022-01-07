from . import App, Config

config = Config()

with App(config=config) as app:
    print(f"Session running at http://localhost:{app.session.port}")
    app.session.wait()
