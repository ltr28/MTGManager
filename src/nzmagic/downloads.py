import datetime
import json
import sqlite3
from pathlib import Path

import pandas as pd
import requests


DB_NAME = "db.sqlite3"


def create_sql(filepath: str):
    df = pd.read_parquet(filepath)
    df.set_index("id", inplace=True)
    df["date"] = "240625"

    db_connection = sqlite3.connect(DB_NAME)
    df.to_sql(name="cardkingdom", con=db_connection)


class CardKingdom:
    MODULE_PATH = Path(__file__).parent.parent.parent
    NAME = "ck"

    def __init__(self):
        downloads_path = Path(self.MODULE_PATH, "downloads")
        if not downloads_path.exists():
            downloads_path.mkdir()

        self.base_path = Path(self.MODULE_PATH, "downloads", self.NAME)
        if not self.base_path.exists():
            self.base_path.mkdir()

    def get_price_data(self):
        """Retrieves data from each URL provided."""
        new_file = Path(self.base_path, f"{datetime.date.today().strftime('%y%m%d')}.parquet")
        if not new_file.exists():
            pricelist_url = "https://api.cardkingdom.com/api/pricelist"
            json_data = requests.get(pricelist_url, timeout=20).json()
            df = pd.DataFrame(json_data["data"])
            df.to_parquet(new_file)

        return pd.read_parquet(new_file)


class Scryfall:
    MODULE_PATH = Path(__file__).parent.parent.parent
    NAME = "scryfall"

    def __init__(self):
        # Create Paths if required
        downloads_path = Path(self.MODULE_PATH, "downloads")
        if not downloads_path.exists():
            downloads_path.mkdir()

        self.base_path = Path(self.MODULE_PATH, "downloads", self.NAME)
        if not self.base_path.exists():
            self.base_path.mkdir()

    def get_symbols(self):
        symbols_url = "https://api.scryfall.com/symbology"
        new_file = Path(self.base_path, "symbols.json")
        if not new_file.exists():
            json_data = requests.get(symbols_url, timeout=20).json()
            with open(new_file, "w", encoding="UTF8") as file:
                json.dump(json_data, file, indent=4)
        return json_data


if __name__ == "__main__":
    scryfall = Scryfall()
    scryfall.get_symbols()
