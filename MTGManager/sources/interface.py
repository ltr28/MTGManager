import datetime
from pathlib import Path

import pandas as pd
import requests
import sqlite3


class SourceInterface:
    URLS = []

    def __init__(self, **kwargs: dict):
        self.name = kwargs.pop("name", "base")
        self.urls = kwargs.pop("urls", [])

        module_path = Path(__file__).parent.parent.parent

        # Create Paths if required
        downloads_path = Path(module_path, "downloads")
        if not downloads_path.exists():
            downloads_path.mkdir()

        self.base_path = Path(module_path, "downloads", self.name)
        if not self.base_path.exists():
            self.base_path.mkdir()

    def get_data(self, urls: list = None):
        """Retrieves data from each URL provided."""
        if urls is None:
            urls = self.URLS

        data = []
        for url in urls:
            new_file = Path(self.base_path, f"{datetime.date.today().strftime('%y%m%d')}.parquet")
            if not new_file.exists():
                json_data = requests.get(url, timeout=20).json()
                df = self.json_to_df(json_data)
                df.to_parquet(new_file)
                data.append(json_data)
        return data

    def json_to_df(self, json_data: pd.DataFrame):
        raise NotImplementedError("Implement the json_to_df function")

    def save_to_database(self, json_data):
        raise NotImplementedError("Classes to implement add to database")
