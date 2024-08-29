import pandas as pd
import numpy as np
from logs.log_manager import LogManager

logger = LogManager('ema_logs').get_logger()

def calculate_ema(df, period=14):
    """
    Calculate the Exponential Moving Average (EMA) for a given DataFrame.

    :param df: DataFrame with 'close' prices.
    :param period: Period for EMA calculation.
    :return: DataFrame with EMA values.
    """
    if len(df) < period:
        logger.warning("Insufficient data for EMA calculation.")
        return df

    if period <= 0:
        logger.error(f"Invalid period: {period}. Period must be positive.")
        raise ValueError("Period must be positive")

    df['ema'] = df['close'].ewm(span=period, adjust=False).mean()

    logger.info("EMA calculation completed.")
    return df
