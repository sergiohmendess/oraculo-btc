import pandas as pd

def rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def sma(series, period=20):
    return series.rolling(period).mean()

def ema(series, period=20):
    return series.ewm(span=period, adjust=False).mean()
