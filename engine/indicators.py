# indicators.py
import pandas as pd

def sma(series, period):
    """Simple Moving Average"""
    return series.rolling(window=period).mean()

def ema(series, period):
    """Exponential Moving Average"""
    return series.ewm(span=period, adjust=False).mean()

def rsi(series, period=14):
    """Relative Strength Index"""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
