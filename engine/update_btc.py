import requests
import pandas as pd
import os
from datetime import datetime

DATA_PATH = "data/btc_5m.csv"
SYMBOL = "BTCUSDT"
INTERVAL = "5m"
LIMIT = 1000

def update_data():
    try:
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": SYMBOL,
            "interval": INTERVAL,
            "limit": LIMIT
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data, columns=[
            "open_time","open","high","low","close","volume",
            "close_time","qav","num_trades",
            "taker_base_vol","taker_quote_vol","ignore"
        ])

        df = df[["open_time","open","high","low","close","volume"]]

        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")

        for col in ["open","high","low","close","volume"]:
            df[col] = df[col].astype(float)

        os.makedirs("data", exist_ok=True)
        df.to_csv(DATA_PATH, index=False)

        print("✅ Dados atualizados:", datetime.now())

    except Exception as e:
        print("❌ Erro atualização:", e)

if __name__ == "__main__":
    update_data()