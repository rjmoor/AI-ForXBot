import pandas as pd

def calculate_stochastic(df, period=14):
    """
    Calculate the Stochastic Oscillator for a given DataFrame.
    
    :param df: DataFrame with 'high', 'low' and 'close' prices.
    :param period: Period for Stochastic Oscillator calculation.
    :return: DataFrame with Stochastic Oscillator values.
    """
    df[f'low_{str(period)}'] = df['low'].rolling(window=period).min()
    df[f'high_{str(period)}'] = df['high'].rolling(window=period).max()
    df['stoch'] = (
        (df['close'] - df[f'low_{str(period)}'])
        / (df[f'high_{str(period)}'] - df[f'low_{str(period)}'])
        * 100
    )
    return df