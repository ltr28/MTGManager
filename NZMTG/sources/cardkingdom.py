#!/usr/bin/python

import pandas as pd

from NZMTG.sources import SourceInterface


class CardKingdom(SourceInterface):
    """
    Retrieves Price Information from Card Kingdom's API.
    """

    def __init__(self, **kwargs):
        urls = ["https://api.cardkingdom.com/api/pricelist"]
        super().__init__(name="ck", urls=urls, **kwargs)

    def json_to_df(self, json_data: dict):
        """
        Converts the json response into a pandas DataFrame

        Args:
            json_data (dict[dicts]): A json file containing CardKingdom pricing data

        Returns:
            pandas.DataFrame: _description_
        """
        df = pd.DataFrame(json_data["data"])

        conversion_dict = {
            "price_sell": {
                "name": "price_retail",
                "type": "float64",
            },
            "price_buylist": {
                "name": "price_buy",
                "type": "float64",
            },
            "qty_sell": {
                "name": "qty_retail",
                "type": "int",
            },
            "qty_buylist": {
                "name": "qty_buylist",
                "type": "int",
            },
        }

        for column, column_conversion in conversion_dict.items():
            df[column_conversion["name"]] = df[column].astype(column_conversion["type"])
        return df

    def save_to_database(self, json_data: dict):
        """
        Save CardKingdom prices from today into the database.
        """
        pass
