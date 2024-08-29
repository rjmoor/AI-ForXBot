import pandas as pd

def calculate_rsi(df, period=14):
    """
    Calculate the Relative Strength Index (RSI) for a given DataFrame.

    :param df: DataFrame with 'close' prices.
    :param period: Period for RSI calculation.
    :return: DataFrame with RSI values.
    """
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    return df
