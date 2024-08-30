import pandas as pd
import numpy as np
from logs.log_manager import LogManager

def calculate_bollinger_bands(df, period=20, std=2):
    logger = LogManager('bollinger_bands_logs').get_logger()
    """
    Calculate the Bollinger Bands for a given DataFrame.
    
    :param df: DataFrame with 'close' prices.
    :param period: Period for Bollinger Bands calculation.
    :param std: Standard deviation for Bollinger Bands calculation.
    :return: DataFrame with Bollinger Bands values.
    """
    if len(df) < period:
        logger.warning("Insufficient data for Bollinger Bands calculation.")
        return df

    if period <= 0:
        logger.error(f"Invalid period: {period}. Period must be positive.")
        raise ValueError("Period must be positive")

    df['sma'] = df['close'].rolling(window=period).mean()
    df['std_dev'] = df['close'].rolling(window=period).std()

    df['middle_5'] = df['sma']
    df['upper_5'] = df['sma'] + (df['std_dev'] * std)
    df['lower_5'] = df['sma'] - (df['std_dev'] * std)

    logger.info("Bollinger Bands calculation completed.")
    return df
