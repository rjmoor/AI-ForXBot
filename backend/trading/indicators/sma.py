import pandas as pd

def calculate_sma(df, period=20):
    """
    Calculate the Simple Moving Average (SMA) for a given DataFrame.

    :param df: DataFrame with 'close' prices.
    :param period: Period for SMA calculation.
    :return: DataFrame with SMA values.
    """
    df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
    return df
