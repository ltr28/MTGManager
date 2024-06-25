import datetime
from pathlib import Path

import pandas as pd
import requests

CK_URL = "https://api.cardkingdom.com/api/pricelist"


class CardKingdom:
    def __init__(self):
        self.name = "ck"
        module_path = Path(__file__).parent.parent.parent

        # Create Paths if required
        downloads_path = Path(module_path, "downloads")
        if not downloads_path.exists():
            downloads_path.mkdir()

        self.base_path = Path(module_path, "downloads", self.name)
        if not self.base_path.exists():
            self.base_path.mkdir()

    def get_data(self):
        """Retrieves data from each URL provided."""
        new_file = Path(
            self.base_path, f"{datetime.date.today().strftime('%y%m%d')}.parquet"
        )
        if not new_file.exists():
            json_data = requests.get(CK_URL, timeout=20).json()
            df = pd.DataFrame(json_data["data"])
            df.to_parquet(new_file)

        return pd.read_parquet(new_file)
