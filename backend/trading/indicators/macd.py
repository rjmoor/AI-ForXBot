import pandas as pd
import numpy as np
from logs.log_manager import LogManager

logger = LogManager('macd_logs').get_logger()

def calculate_macd(df, short_period=12, long_period=26, signal_period=9):
    """
    Calculate the Moving Average Convergence Divergence (MACD) for a given DataFrame.

    :param df: DataFrame with 'close' prices.
    :param short_period: Short period for MACD calculation.
    :param long_period: Long period for MACD calculation.
    :param signal_period: Signal period for MACD calculation.
    :return: DataFrame with MACD values.
    """
    if len(df) < long_period:
        logger.warning("Insufficient data for MACD calculation.")
        return df

    if short_period <= 0 or long_period <= 0 or signal_period <= 0:
        logger.error("Invalid period(s). Periods must be positive.")
        raise ValueError("Periods must be positive")

    df['ema_short'] = df['close'].ewm(span=short_period, adjust=False).mean()
    df['ema_long'] = df['close'].ewm(span=long_period, adjust=False).mean()
    df['macd'] = df['ema_short'] - df['ema_long']
    df['signal'] = df['macd'].ewm(span=signal_period, adjust=False).mean()
    df['histogram'] = df['macd'] - df['signal']

    logger.info("MACD calculation completed.")
    return df
