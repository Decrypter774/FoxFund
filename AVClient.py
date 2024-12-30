import json
import os
import requests

class AVClient:
    api_key:str = ""
    base_url:str=""
    def __init__(self, av_api_key):
        self.api_key=av_api_key
        self.base_url = "https://www.alphavantage.co/query"

    def _make_request(self, params):
        """
        Makes a request to the Alpha Vantage API.

        Args:
            params (dict): A dictionary of parameters for the API request.

        Returns:
            dict or None: The JSON response from the API, or None if the request fails.
        """
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


    def get_global_quote(self, symbol):
        """
        Retrieves the global quote data for a given stock symbol.

        Args:
            symbol (str): The stock symbol (e.g., 'AAPL').

        Returns:
            dict or None: A dictionary containing the global quote data, or None if the request fails.
        """
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol
        }
        return self._make_request(params)


    def get_income_statement(self, symbol):
        """
        Retrieves the income statement data for a given stock symbol.

         Args:
             symbol (str): The stock symbol (e.g., 'AAPL').

        Returns:
             dict or None: A dictionary containing the income statement data, or None if the request fails.
        """
        params = {
            "function": "INCOME_STATEMENT",
             "symbol": symbol
         }
        return self._make_request(params)

    def get_overview(self, symbol):
        params = {
            "function": "OVERVIEW",
             "symbol": symbol
         }
        return self._make_request(params)