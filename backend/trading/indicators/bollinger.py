import pandas as pd

def calculate_bollinger_bands(df, period=20, std=2):
    """
    Calculate the Bollinger Bands for a given DataFrame.
    
    :param df: DataFrame with 'close' prices.
    :param period: Period for Bollinger Bands calculation.
    :param std: Standard deviation for Bollinger Bands calculation.
    :return: DataFrame with Bollinger Bands values.
    """
    df[f'middle_{period}'] = df['close'].rolling(window=period).mean()
    df[f'upper_{period}'] = df[f'middle_{period}'] + (df['close'].rolling(window=period).std() * std)
    df[f'lower_{period}'] = df[f'middle_{period}'] - (df['close'].rolling(window=period).std() * std)
    return df