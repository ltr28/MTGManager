import datetime
import sqlite3
from pathlib import Path

import pandas as pd
import requests

CK_URL = "https://api.cardkingdom.com/api/pricelist"


DB_NAME = "db.sqlite3"


def create_sql(filepath: str):

    # filepath = "downloads/ck/240625.parquet"
    df = pd.read_parquet(filepath)
    df.set_index("id", inplace=True)
    df["date"] = "240625"

    db_connection = sqlite3.connect(DB_NAME)
    df.to_sql(name="cardkingdom", con=db_connection)


class CardKingdom:
    MODULE_PATH = Path(__file__).parent.parent.parent
    NAME = "ck"

    def __init__(self):
        # Create Paths if required
        downloads_path = Path(self.MODULE_PATH, "downloads")
        if not downloads_path.exists():
            downloads_path.mkdir()

        self.base_path = Path(self.MODULE_PATH, "downloads", self.NAME)
        if not self.base_path.exists():
            self.base_path.mkdir()

    def get_data(self):
        """Retrieves data from each URL provided."""
        new_file = Path(self.base_path, f"{datetime.date.today().strftime('%y%m%d')}.parquet")
        if not new_file.exists():
            json_data = requests.get(CK_URL, timeout=20).json()
            df = pd.DataFrame(json_data["data"])
            df.to_parquet(new_file)

        return pd.read_parquet(new_file)
