import json
import os
import requests

class FMPClient:
    def __init__(self, api_key):
        self.base_url = "https://financialmodelingprep.com/api/v3/stock-screener"
        self.api_key=api_key
    def _make_request(self, params):
        params['apikey'] = self.api_key
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            return None
    def get_stock_list(self):
        params = {
            "marketCapRange":"1000000000%3A5000000000",
            "industry":"Technology",
            "apikey":self.api_key
        }
        return self._make_request(params)