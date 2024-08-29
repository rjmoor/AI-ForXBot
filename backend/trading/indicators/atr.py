import pandas as pd

def calculate_atr(df, df_original, period=14):
    """
    Calculate the Average True Range (ATR) for a given DataFrame.
    
    :param df: DataFrame with 'high', 'low' and 'close' prices.
    :param period: Period for ATR calculation.
    :return: DataFrame with ATR values.
    """
    df['h-l'] = df['high'] - df['low']
    df['h-yc'] = abs(df['high'] - df['close'].shift())
    df['l-yc'] = abs(df['low'] - df['close'].shift())
    df['tr'] = df[['h-l', 'h-yc', 'l-yc']].max(axis=1)
    df['atr'] = df['tr'].rolling(window=period).mean()
    df = df.drop(['h-l', 'h-yc', 'l-yc', 'tr'], axis=1)
    df = pd.concat([df_original, df['atr']], axis=1)
    return df