import json
import time
import os
import requests

class FMPClient:
    def __init__(self, api_key):
        self.base_url = "https://financialmodelingprep.com/api/v3/stock-screener"
        self.api_key=api_key

    def _make_request(self, params):
        params['apikey'] = self.api_key
        try:
            url = self.base_url
            response = requests.get(url, params=params)
            if response.status_code == 429:
                time.sleep(5)
                response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            return None

    def get_stock_list(self, industry: str, market_cap_from: float, market_cap_to: float):
        params = {
            "marketCapRange": str(market_cap_from) + "%3A" + str(market_cap_to),
            "country":"US",
            "industry":industry,
        }
        return self._make_request(params)