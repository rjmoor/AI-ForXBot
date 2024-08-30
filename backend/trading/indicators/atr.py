import pandas as pd
import numpy as np
from logs.log_manager import LogManager

logger = LogManager('macd_logs').get_logger()

def calculate_atr(df, df_original, period=14):
    """
    Calculate the Average True Range (ATR) for a given DataFrame.
    
    :param df: DataFrame with 'high', 'low' and 'close' prices.
    :param period: Period for ATR calculation.
    :return: DataFrame with ATR values.
    """
    if len(df) < period:
        logger.warning("Insufficient data for ATR calculation.")
        return df

    if period <= 0:
        logger.error(f"Invalid period: {period}. Period must be positive.")
        raise ValueError("Period must be positive")

    df['high-low'] = df['high'] - df['low']
    df['high-close'] = (df['high'] - df['close'].shift()).abs()
    df['low-close'] = (df['low'] - df['close'].shift()).abs()
    df['true_range'] = np.max([df['high-low'], df['high-close'], df['low-close']], axis=0)
    df['atr'] = df['true_range'].ewm(span=period, adjust=False).mean()

    logger.info("ATR calculation completed.")
    return df