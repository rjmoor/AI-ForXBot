import pandas as pd
import numpy as np
from logs.log_manager import LogManager

logger = LogManager('rsi_logs').get_logger()

def calculate_rsi(df, period=14):
    """
    Calculate the Relative Strength Index (RSI) for a given DataFrame.

    :param df: DataFrame with 'close' prices.
    :param period: Period for RSI calculation.
    :return: DataFrame with RSI values.
    """
    if len(df) < period:
        logger.warning("Insufficient data for RSI calculation.")
        return df

    if period <= 0:
        logger.error(f"Invalid period: {period}. Period must be positive.")
        raise ValueError("Period must be positive")

    df['delta'] = df['close'].diff()
    df['gain'] = df['delta'].apply(lambda x: max(x, 0))
    df['loss'] = df['delta'].apply(lambda x: -x if x < 0 else 0)

    avg_gain = df['gain'].rolling(window=period, min_periods=1).mean()
    avg_loss = df['loss'].rolling(window=period, min_periods=1).mean()

    # Avoid division by zero
    avg_loss.replace(0, np.nan, inplace=True)
    rs = avg_gain / avg_loss
    df['rsi'] = 100 - (100 / (1 + rs))

    logger.info("RSI calculation completed.")
    return df
