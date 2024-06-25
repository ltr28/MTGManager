import sqlite3

import pandas as pd


DB_NAME = "db.sqlite3"


def create_sql(filepath: str):

    # filepath = "downloads/ck/240625.parquet"
    df = pd.read_parquet(filepath)
    df.set_index("id", inplace=True)
    df["date"] = "240625"

    db_connection = sqlite3.connect(DB_NAME)
    df.to_sql(name="cardkingdom", con=db_connection)
