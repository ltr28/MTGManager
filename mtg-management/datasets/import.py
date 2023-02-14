import json
from pathlib import Path
import requests

class BaseDataSource:
    def __init__(self, **kwargs: dict):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
            
        if not hasattr(self, 'urls'):
            self.urls = {}
            
        self.base_path = Path('data', self.name)
        if not self.base_path.exists():
            self.base_path.mkdir()

    def get_data(self, filename: str):
        """ Retrieves data from url"""
        
        for filename, url in self.urls.items():
            save_filepath = Path(self.base_path, filename)
            if save_filepath.is_file():
                continue
            
            response = requests.get(url)
            with open(save_filepath, 'w') as save_file:
                try:
                    json.dump(response.json(), save_file, indent=4, sort_keys=True)
                except:
                    continue
        
        return save_filepath
        
    def get_name():
        return 'base'
    
    @property
    def name(self):
        return self.get_name()
            

    
class CardKingdomSource(BaseDataSource):
    
    def get_name(self):
        return 'ck'
    

def save_ck_data():
    ck_urls = {
        'pricelist': "https://api.cardkingdom.com/api/pricelist"
    }
    
    ck_data = CardKingdomSource(urls=ck_urls)
    print(ck_data)

if __name__ == "__main__":
    save_ck_data()