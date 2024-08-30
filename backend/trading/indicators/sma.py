import pandas as pd
import numpy as np
from logs.log_manager import LogManager

def calculate_sma(df, period=5):
    logger = LogManager('sma_logs').get_logger()
    """
    Calculate the Simple Moving Average (SMA) for a given DataFrame.

    :param df: DataFrame with 'close' prices.
    :param period: Period for SMA calculation.
    :return: DataFrame with SMA values.
    """
    if period <= 0:
        logger.error(f"Invalid period: {period}. Period must be positive.")
        raise ValueError("Period must be positive")

    df[f'sma_{period}'] = df['close'].rolling(window=period).mean()

    logger.info("SMA calculation completed.")
    return df

