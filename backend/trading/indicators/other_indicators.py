import pandas as pd
import numpy as np
from logs.log_manager import LogManager

"""
Calculate the Average Directional Index (ADX) for a given DataFrame. The ADX is a trend strength indicator that measures the strength of a trend, regardless of its direction.
"""
"""
:param df: DataFrame with 'high', 'low', 'close' prices.
:param period: Period for ADX calculation.
:return: DataFrame with ADX values.
"""
def calculate_adx(df, period=14):
    logger = LogManager('adx_logs').get_logger()

    if period <= 0:
        logger.error(f"Invalid period: {period}. Period must be positive.")
        raise ValueError("Period must be positive")

    if len(df) < period:
        logger.warning("Insufficient data for ADX calculation.")
        return df

    # Calculate differences
    df['high_diff'] = df['high'].diff()
    df['low_diff'] = df['low'].diff()

    # Calculate directional movements
    df['plus_dm'] = df['high_diff'].where((df['high_diff'] > df['low_diff']) & (df['high_diff'] > 0), 0)
    df['minus_dm'] = -df['low_diff'].where((df['low_diff'] > df['high_diff']) & (df['low_diff'] > 0), 0)

    # Smooth the directional movements
    df['plus_dm_smooth'] = df['plus_dm'].rolling(window=period, min_periods=1).sum()
    df['minus_dm_smooth'] = df['minus_dm'].rolling(window=period, min_periods=1).sum()

    # Calculate True Range
    df['tr'] = pd.concat([
        df['high'] - df['low'],
        (df['high'] - df['close'].shift(1)).abs(),
        (df['low'] - df['close'].shift(1)).abs()
    ], axis=1).max(axis=1)

    # Smooth the True Range
    df['tr_smooth'] = df['tr'].rolling(window=period, min_periods=1).sum()

    # Calculate Directional Indicators
    df['plus_di'] = 100 * (df['plus_dm_smooth'] / df['tr_smooth'])
    df['minus_di'] = 100 * (df['minus_dm_smooth'] / df['tr_smooth'])

    # Calculate DX and ADX
    df['dx'] = 100 * abs(df['plus_di'] - df['minus_di']) / (df['plus_di'] + df['minus_di'])
    df['adx'] = df['dx'].rolling(window=period, min_periods=1).mean()

    # Drop rows with NaN values
    df.dropna(inplace=True)

    logger.info("ADX calculation completed.")
    return df


"""
    Calculate the Aroon Indicator for a given DataFrame. The Aroon Indicator is a trend-following indicator that measures the time between highs and lows over a given period.
"""
"""
    :param df: DataFrame with 'high', 'low' prices.
    :param period: Period for Aroon calculation.
    :return: DataFrame with Aroon values.
"""

def calculate_aroon(df, period=14):
    logger = LogManager('aroon_indicator_logs').get_logger()
    
    if len(df) < period:
        logger.warning("Insufficient data for Aroon calculation.")
        return df

    if period <= 0:
        logger.error(f"Invalid period: {period}. Period must be positive.")
        raise ValueError("Period must be positive")

    required_columns = ['high', 'low']
    for col in required_columns:
        if col not in df.columns:
            logger.error(f"Missing column: {col}")
            raise KeyError(f"Missing column: {col}")

    df['aroon_up'] = 100 * df['high'].rolling(window=period).apply(lambda x: np.argmax(x) / len(x), raw=True)
    df['aroon_down'] = 100 * df['low'].rolling(window=period).apply(lambda x: np.argmin(x) / len(x), raw=True)

    logger.info("Aroon calculation completed.")
    return df


"""
Calculate the Commodity Channel Index (CCI) for a given DataFrame. The CCI is calculated using the typical price, which is the average of the high, low, and close prices. The CCI measures the difference between the typical price and its simple moving average, relative to the mean deviation.
"""
"""
:param df: DataFrame with 'high', 'low', 'close' prices.
:param period: Period for CCI calculation.
:return: DataFrame with CCI values.
"""
def calculate_cci(df, period=14):
    logger = LogManager('cci_indicator_logs').get_logger()
    
    if len(df) < period:
        logger.warning("Insufficient data for CCI calculation.")
        return df

    if period <= 0:
        logger.error(f"Invalid period: {period}. Period must be positive.")
        raise ValueError("Period must be positive")

    required_columns = ['high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            logger.error(f"Missing column: {col}")
            raise KeyError(f"Missing column: {col}")

    df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
    df['sma'] = df['typical_price'].rolling(window=period).mean()
    df['mean_deviation'] = df['typical_price'].rolling(window=period).apply(lambda x: np.mean(np.abs(x - np.mean(x))))
    df['cci'] = (df['typical_price'] - df['sma']) / (0.015 * df['mean_deviation'])

    logger.info("CCI calculation completed.")
    return df



"""
    Calculate the Money Flow Index (MFI) for a given DataFrame. The MFI is a momentum indicator that measures the inflow and outflow of money into a security.
"""
"""
    :param df: DataFrame with 'high', 'low', 'close', 'volume' prices.
    :param period: Period for MFI calculation.
    :return: DataFrame with MFI values.
"""
def calculate_mfi(df, period=14):
    logger = LogManager('mfi_indicator_indicator_logs').get_logger()

    required_columns = ['high', 'low', 'close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            logger.error(f"Missing column: {col}")
            raise KeyError(f"Missing column: {col}")

    df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
    df['money_flow'] = df['typical_price'] * df['volume']
    df['money_flow_pos'] = df['money_flow'].where(df['typical_price'].diff() > 0, 0)
    df['money_flow_neg'] = df['money_flow'].where(df['typical_price'].diff() < 0, 0)
    
    df['money_flow_pos_sum'] = df['money_flow_pos'].rolling(window=period).sum()
    df['money_flow_neg_sum'] = df['money_flow_neg'].rolling(window=period).sum()
    
    df['mfi'] = 100 * (df['money_flow_pos_sum'] / (df['money_flow_pos_sum'] + df['money_flow_neg_sum']))
    
    logger.info("MFI calculation completed.")
    return df


"""
Calculate the On-Balance Volume (OBV) for a given DataFrame. The OBV is the running total of positive and negative volume. A buy signal is generated when the OBV crosses above its moving average, and a sell signal is generated when the OBV crosses below its moving average.
"""
"""
:param df: DataFrame with 'close', 'volume' prices.
:return: DataFrame with OBV values.
"""
def calculate_obv(df):
    logger = LogManager('obv_indicator_logs').get_logger()
    if 'volume' not in df.columns:
        logger.error("Volume column missing from DataFrame.")
        raise ValueError("DataFrame must contain a 'volume' column")

    df['obv'] = df['volume'].where(df['close'] > df['close'].shift(1), -df['volume'])
    df['obv'] = df['obv'].cumsum()

    logger.info("OBV calculation completed.")
    return df


"""
    Calculate the Volume Weighted Average Price (VWAP) for a given DataFrame. The VWAP is a trading benchmark used by traders that gives the average price a security has traded at throughout the day, based on both volume and price.
"""
"""
    :param df: DataFrame with 'high', 'low', 'close', 'volume' prices.
    :return: DataFrame with VWAP values.
"""
def calculate_vwap(df):
    logger = LogManager('vwap_indicator_logs').get_logger()
    
    # Check if the required column is in the DataFrame
    if 'volume' not in df.columns:
        logger.error("Volume column missing from DataFrame.")
        raise ValueError("DataFrame must contain a 'volume' column")

    # Check if required columns are present
    required_columns = ['high', 'low', 'close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            logger.error(f"Missing column: {col}")
            raise KeyError(f"Missing column: {col}")

    df['vwap'] = (df['high'] + df['low'] + df['close']) / 3 * df['volume']
    df['vwap'] = df['vwap'].cumsum() / df['volume'].cumsum()

    logger.info("VWAP calculation completed.")
    return df



"""
    Calculate the Williams %R for a given DataFrame. The Williams %R is a momentum indicator that measures the level of the close relative to the high-low range over a given period.
"""
"""
    :param df: DataFrame with 'high', 'low', 'close' prices.
    :param period: Period for Williams %R calculation.
    :return: DataFrame with Williams %R values.
"""
def calculate_williams_r(df, period=14):
    logger = LogManager('williams_r_indicator_logs').get_logger()
    
    # Check if required columns are in the DataFrame
    required_columns = ['high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            logger.error(f"Missing column: {col}")
            raise KeyError(f"Missing column: {col}")

    if period <= 0:
        logger.error(f"Invalid period: {period}. Period must be positive.")
        raise ValueError("Period must be positive")

    df['max_high'] = df['high'].rolling(window=period).max()
    df['min_low'] = df['low'].rolling(window=period).min()

    df['williams_r'] = -100 * ((df['max_high'] - df['close']) / (df['max_high'] - df['min_low']))

    logger.info("Williams %R calculation completed.")
    return df



"""
    Calculate the Average True Range (ATR) for a given DataFrame.
"""
"""
    :param df: DataFrame with 'high', 'low' and 'close' prices.
    :param period: Period for ATR calculation.
    :return: DataFrame with ATR values.
""" 
def calculate_atr(df, period=14):
    logger = LogManager('atr_indicator_logs').get_logger()
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

    """
    Calculate the Stochastic Oscillator for a given DataFrame.
    """
