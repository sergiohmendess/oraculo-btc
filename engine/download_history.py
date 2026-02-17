import requests
import pandas as pd
from datetime import datetime

def download_btc_history(interval="1h", limit=1000):
    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": "BTCUSDT",
        "interval": interval,
        "limit": limit
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception("Erro ao baixar dados da Binance")

    data = response.json()

    rows = []

    for candle in data:
        rows.append({
            "timestamp": datetime.fromtimestamp(candle[0]/1000),
            "open": float(candle[1]),
            "high": float(candle[2]),
            "low": float(candle[3]),
            "close": float(candle[4]),
            "volume": float(candle[5]),
        })

    df = pd.DataFrame(rows)

    df.to_csv("data/btc_base.csv", index=False)

    print("✅ Histórico BTC baixado com sucesso!")

if __name__ == "__main__":
    download_btc_history()