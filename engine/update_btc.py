# engine/update_btc.py

import requests
import pandas as pd
from datetime import datetime
import os

CMC_API_KEY = "9e63a969fe4d40528c3d4c7945050173"

def fetch_price():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY,
    }

    params = {
        "symbol": "BTC",
        "convert": "USD"
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)

    if response.status_code != 200:
        raise Exception(f"Erro API CMC: {response.status_code}")

    data = response.json()
    price = data["data"]["BTC"]["quote"]["USD"]["price"]
    return float(price)


def update_csv():

    file_path = "data/btc_base.csv"

    price = fetch_price()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_row = pd.DataFrame([{
        "timestamp": timestamp,
        "open": price,
        "high": price,
        "low": price,
        "close": price,
        "volume": 0
    }])

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)

        # 🔥 CORREÇÃO AQUI
        if not df.empty and df.iloc[-1]["timestamp"] == timestamp:
            print("⏳ Já atualizado neste minuto")
            return

        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row

    df.to_csv(file_path, index=False)

    print(f"✅ CSV atualizado com preço {price:.2f} USD em {timestamp}")