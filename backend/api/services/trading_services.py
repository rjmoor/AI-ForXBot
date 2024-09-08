# backend/api/services/trading_services.py
import threading
import time
from logs.log_manager import LogManager
from trading.brokers.oanda_client import OandaClient
from trading.managers import manager
from data.repositories.mongo import MongoDBHandler

'''
Handles requests and interacts with services. Contains the core service logic.
The TradingService module manages trading logic and state. It provides methods to start, stop, and check the status of trading processes.
'''

class TradingService:
    def __init__(self):
        """
        Initializes the TradingService with default state.
        """
        self.is_trading = False
        self.trade_thread = None
        self.mongo_handler = MongoDBHandler(db_name="trading_db", collection_name="trades")
        self.oanda_client = OandaClient()
        self.logger = LogManager('trading_service').get_logger()

    def start_trading(self):
        """
        Starts the trading process by initializing the trading manager and running the trading logic in a separate thread.
        """
        manager.initialize()
        if not self.is_trading:
            self.is_trading = True
            self.trade_thread = threading.Thread(target=self._trading_logic)
            self.trade_thread.start()
            self.logger.info("Trading process started.")
        else:
            self.logger.warning("Trading is already active.")

    def stop_trading(self):
        """
        Stops the trading process by terminating the trading manager and waiting for the trading thread to finish.
        """
        manager.terminate()
        if self.is_trading:
            self.is_trading = False
            if self.trade_thread:
                self.trade_thread.join()  # Wait for the trading thread to finish
            self.logger.info("Trading process stopped.")
        else:
            self.logger.warning("Trading is not active.")

    def log_trade(self, trade_data):
        """
        Logs the trade in the MongoDB collection.

        :param trade_data: A dictionary containing trade details.
        :return: The inserted ID of the trade.
        """
        trade_id = self.mongo_handler.create(trade_data)
        if trade_id:
            self.logger.info(f"Trade logged with ID: {trade_id}")
        else:
            self.logger.warning("Trade not logged due to duplicate or error.")
        return trade_id

    def place_trade(self, trade_data):
        """
        Places a trade with the OANDA broker and logs it in the database.

        :param trade_data: A dictionary containing trade details to place.
        :return: A dictionary containing the OANDA API response.
        """
        try:
            oanda_response = self.oanda_client.place_order(trade_data)
            self.log_trade(trade_data)
            self.logger.info(f"Trade placed successfully: {oanda_response}")
            return oanda_response
        except Exception as e:
            self.logger.error(f"Error placing trade: {e}")
            raise

    def get_status(self):
        """
        Retrieves the current status of the trading process.

        :return: A dictionary indicating whether trading is active or not.
        """
        status = {'status': 'Running'} if self.is_trading else {'status': 'Not Started'}
        if manager.is_running():
            self.logger.info("Trading manager is running.")
        else:
            self.logger.warning("Trading manager is not running.")
        return status

    def _trading_logic(self):
        """
        Contains the logic for trading. This method runs in a separate thread and handles the actual trading operations.
        """
        while self.is_trading:
            # Implement your trading logic here
            self.logger.info("Executing trading logic...")
            time.sleep(5)  # Example sleep to simulate trading work

# Initialize a global instance of TradingService
trading_service = TradingService()

