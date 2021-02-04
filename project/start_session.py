import atoti as tt
import pandas as pd


def start_session():
    session = tt.create_session(config="config.yml")
    store = session.read_pandas(
        pd.DataFrame(
            columns=["Product", "Price"],
            data=[
                ("car", 20000.0),
                ("computer", 1000.0),
                ("phone", 500.0),
                ("game", 60.0),
            ],
        ),
        store_name="Products",
    )
    session.create_cube(store)
    return session
