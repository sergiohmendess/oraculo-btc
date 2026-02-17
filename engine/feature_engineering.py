# feature_engineering.py
from engine.indicators import sma, ema, rsi

def create_features(df):
    if 'rsi14' not in df.columns:
        df['rsi14'] = rsi(df['close'], period=14)
    if 'sma20' not in df.columns:
        df['sma20'] = sma(df['close'], period=20)
    if 'ema20' not in df.columns:
        df['ema20'] = ema(df['close'], period=20)
    if 'ret' not in df.columns:
        df['ret'] = df['close'].pct_change()
    return df
