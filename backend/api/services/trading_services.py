import threading
import time

from logs.log_manager import LogManager
from trading.brokers.oanda_client import OandaClient
from trading.managers import manager
from data.repositories.mongo import get_database

'''
Handles requests and interacts with services. Contains the core service logic.
The trading_service module manages trading logic and state. It provides methods to start, stop, and check the status of trading processes.
'''

class TradingService:
    def __init__(self):
        """
        Initializes the TradingService with default state.
        """
        self.is_trading = False
        self.trade_thread = None

    def start_trading(self):
        """
        Starts the trading process by initializing the trading manager and running the trading logic in a separate thread.
        """
        manager.initialize()
        if not self.is_trading:
            self.is_trading = True
            self.trade_thread = threading.Thread(target=self._trading_logic)
            self.trade_thread.start()

    def stop_trading(self):
        """
        Stops the trading process by terminating the trading manager and waiting for the trading thread to finish.
        """
        manager.terminate()
        if self.is_trading:
            self.is_trading = False
            if self.trade_thread:
                self.trade_thread.join()  # Wait for the trading thread to finish
                
    def log_trade(self, trade_data):
        db = get_database('trading_db')
        trades_collection = db['trades']
        result = trades_collection.insert_one(trade_data)
        return result.inserted_id

    def place_trade(self, trade_data):
        # Implement trade placement logic with the broker here...
        
        # For example, using the OandaClient
        oanda_client = OandaClient()
        oanda_response = oanda_client.place_order(trade_data)
        
        # Log the trade in MongoDB
        self.log_trade(trade_data)
        
        return oanda_response

    def get_status(self):
        """
        Retrieves the current status of the trading process.

        :return: A dictionary indicating whether trading is active or not.
        """
        if self.is_trading:
            return {'status': 'Running'} if manager.is_running() else {'status': 'Stopped'}
        return {'status': 'Not Started'}

    def _trading_logic(self):
        """
        Contains the logic for trading. This method runs in a separate thread and handles the actual trading operations.
        """
        while self.is_trading:
            # Add your trading logic here
            print("Trading...")
            time.sleep(5)  # Example sleep to simulate trading work

# Initialize a global instance of TradingService
trading_service = TradingService()
