import pandas as pd

def calculate_ema(df, period=20):
    """
    Calculate the Exponential Moving Average (EMA) for a given DataFrame.

    :param df: DataFrame with 'close' prices.
    :param period: Period for EMA calculation.
    :return: DataFrame with EMA values.
    """
    df[f'ema_{period}'] = df['close'].ewm(span=period, adjust=False).mean()
    return df
