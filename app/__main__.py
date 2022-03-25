from . import App, Config

config = Config()

with App(config=config) as app:
    print(f"Session listening on port {app.session.port}")
    app.session.wait()
