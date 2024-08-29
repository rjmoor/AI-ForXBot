import pandas as pd

def calculate_macd(df, df_ema_12, df_ema_26):
    """
    Calculate the Moving Average Convergence Divergence (MACD) for a given DataFrame.
    
    :param df: DataFrame with 'close' prices.
    :param df_ema_12: DataFrame with 12-period Exponential Moving Average (EMA) values.
    :param df_ema_26: DataFrame with 26-period Exponential Moving Average (EMA) values.
    :return: DataFrame with MACD values.
    """
    df['macd'] = df_ema_12['ema_12'] - df_ema_26['ema_26']
    df['signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['histogram'] = df['macd'] - df['signal']
    return df