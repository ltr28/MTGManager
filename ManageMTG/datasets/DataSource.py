#!/usr/bin/python

import datetime
from pathlib import Path

import pandas as pd
import requests


class PriceSource:
    def __init__(self, **kwargs: dict):
        self.name = kwargs.pop("name", "base")
        self.urls = kwargs.pop("urls", [])

        module_path = Path(__file__).parent.parent.parent
        self.base_path = Path(module_path, "downloads", self.name)
        if not self.base_path.exists():
            self.base_path.mkdir()

    def get_data(self):
        for url in self.urls:
            new_file = Path(self.base_path, f"{datetime.date.today().strftime('%d%m%y')}.parquet")
            if not new_file.exists():
                json_data = requests.get(url, timeout=20).json()
                df = self.json_to_df(json_data)
                df.to_parquet(new_file)

    def json_to_df(self, json_data: pd.DataFrame):
        raise NotImplementedError("Implement the json_to_df function")


class CardKingdomSource(PriceSource):
    """
    Retrieves Price Information from Card Kingdom's API.
    """

    def __init__(self, **kwargs):
        urls = ["https://api.cardkingdom.com/api/pricelist"]
        super().__init__(name="ck", urls=urls, **kwargs)

    def json_to_df(self, json_data):
        """
        Converts the json response into a pandas DataFrame

        Args:
            json_data (dict[dicts]): A json file containing CardKingdom pricing data

        Returns:
            pandas.DataFrame: _description_
        """
        df = pd.DataFrame(json_data["data"])

        conversion_dict = {
            "price_retail": "float64",
            "price_buy": "float64",
            "qty_retail": "int",
            "qty_buying": "int",
        }

        for column, new_type in conversion_dict.items():
            df[column] = df[column].astype(new_type)
        return df


def main():
    ck_source = CardKingdomSource()
    ck_source.get_data()
    print("Downloaded Card Kingdom")


if __name__ == "__main__":
    main()
