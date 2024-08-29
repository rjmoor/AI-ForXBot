import requests
from config.secrets import defs

'''
Create a module to handle interactions with the OANDA API.
The OandaClient class is a wrapper for the OANDA API, providing methods to interact with it.
'''

class OandaClient:
    def __init__(self, environment='practice'):
        """
        Initializes the OandaClient with the provided environment.

        :param environment: The trading environment to use ('live' or 'practice').
        """
        self.environment = environment
        self.base_url = defs.OANDA_URL_D if environment == 'practice' else defs.OANDA_URL_L
        self.headers = defs.SECURE_HEADER

    def get_account(self):
        """
        Retrieves account details from OANDA.

        :return: A dictionary containing account details.
        """
        url = f'{self.base_url}/accounts/{defs.ACCOUNT_ID}'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def place_order(self, order_data):
        """
        Places a new order with OANDA.

        :param order_data: A dictionary containing order details.
        :return: A dictionary containing the response from OANDA.
        """
        url = f'{self.base_url}/accounts/{defs.ACCOUNT_ID}/orders'
        response = requests.post(url, json=order_data, headers=self.headers)
        return response.json()

    def get_orders(self):
        """
        Retrieves a list of open orders from OANDA.

        :return: A dictionary containing the list of open orders.
        """
        url = f'{self.base_url}/accounts/{defs.ACCOUNT_ID}/orders'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_positions(self):
        """
        Retrieves current positions from OANDA.

        :return: A dictionary containing current positions.
        """
        url = f'{self.base_url}/accounts/{defs.ACCOUNT_ID}/positions'
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_candles(self, instrument, granularity='M1', count=5000):
        """
        Retrieves historical candle data for a specific instrument from OANDA.

        :param instrument: The instrument to retrieve candle data for.
        :param granularity: The granularity of the candle data (e.g., 'M1' for 1-minute).
        :param count: The number of candles to retrieve.
        :return: A dictionary containing the historical candle data.
        """
        url = f'{self.base_url}/instruments/{instrument}/candles'
        params = {
            'granularity': granularity,
            'count': count
        }
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()
