# backend/trading/indicators/rsi.py
import numpy as np
from logs.log_manager import LogManager
from data.repositories.sqlite3 import SQLiteDB
from datetime import datetime

# Configure loggers
logger = LogManager('rsi_logs').get_logger()

class RSI:
    def __init__(self, db_name="indicators.db"):
        """
        Initialize the RSI class with a SQLiteDB handler.

        :param db_name: The name of the SQLite database file.
        """
        self.db_handler = SQLiteDB(db_name=db_name)

    @staticmethod
    def calculate(df, period=14):
        """
        Calculate the Relative Strength Index (RSI) for a given DataFrame.

        :param df: DataFrame with 'close' prices.
        :param period: Lookback period for RSI calculation.
        :return: DataFrame with the RSI values.
        """
        # Ensure the necessary 'close' column exists
        if 'close' not in df.columns:
            logger.error("DataFrame must contain 'close' column.")
            raise KeyError("DataFrame must contain 'close' column.")
        
        # Ensure there is enough data for the RSI calculation
        if len(df) < period:
            logger.warning("Insufficient data for RSI calculation.")
            return df

        # Calculate the price changes
        delta = df['close'].diff()

        # Separate the gains and losses
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        # Calculate the Relative Strength (RS)
        rs = gain / loss

        # Calculate the RSI
        df['rsi'] = 100 - (100 / (1 + rs))

        logger.info(f"RSI calculation for period {period} completed.")
        return df

    def insert_results_to_db(self, indicator_name, instrument, result_df, period):
        """
        Insert the RSI results into the SQLite database.

        :param indicator_name: The name of the indicator (e.g., 'RSI').
        :param instrument: The instrument for which the calculation was made (e.g., 'EUR_USD').
        :param result_df: DataFrame containing the calculated RSI values.
        :param period: Period for which the RSI was calculated.
        """
        indicator_id = self.db_handler.get_indicator_id(indicator_name)
        timestamp = datetime.now().isoformat()

        param_name = 'rsi'
        # Insert RSI results row by row
        for _, row in result_df.iterrows():
            param_value = row['rsi']
            self.db_handler.add_indicator_results(indicator_id, timestamp, param_name, param_value)
            self.db_handler.add_indicator_parameters(indicator_id, {'period': period})

        logger.info(f"Inserted RSI results for {instrument} into SQLite.")
