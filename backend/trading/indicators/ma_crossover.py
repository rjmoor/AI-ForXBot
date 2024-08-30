import pandas as pd
import numpy as np
from logs.log_manager import LogManager

def calculate_moving_average(df, fast_period, slow_period):
    logger = LogManager('ma_logs').get_logger()
    """
    Calculate the Moving Average (MA) for a given DataFrame.

    :param df: DataFrame with 'close' prices.
    :param period: Period for MA calculation.
    :return: DataFrame with MA values.
    """

    # Validate the periods
    if fast_period <= 0 or slow_period <= 0:
        logger.error("Periods must be positive.")
        raise ValueError("Periods must be positive")
    if fast_period >= slow_period:
        logger.error("Fast period must be less than slow period.")
        raise ValueError("Fast period must be less than slow period")

    # Calculate fast and slow moving averages
    df['fast_ma'] = df['close'].rolling(window=fast_period).mean()
    df['slow_ma'] = df['close'].rolling(window=slow_period).mean()

    # Calculate crossover signals
    df['crossover'] = np.where(df['fast_ma'] > df['slow_ma'], 1, 0)
    df['crossover_signal'] = df['crossover'].diff().fillna(0)

    logger.info("Moving Average calculation and crossover detection completed.")
    return df

    
    