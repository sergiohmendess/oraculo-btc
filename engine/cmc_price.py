# engine/cmc_price.py

import requests
import pandas as pd
import os
from datetime import datetime

# SUA API KEY (mantendo como você pediu)
API_KEY = "9e63a969fe4d40528c3d4c7945050173"

# Caminho do CSV
CSV_PATH = os.path.join("data", "btc_base.csv")


def fetch_btc_price():
    """
    Pega o preço atual do BTC em USD e BRL usando CoinMarketCap.
    """

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    params = {
        "symbol": "BTC",
        "convert": "USD,BRL"
    }

    headers = {
        "X-CMC_PRO_API_KEY": API_KEY,
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        price_usd = data["data"]["BTC"]["quote"]["USD"]["price"]
        price_brl = data["data"]["BTC"]["quote"]["BRL"]["price"]

        return float(price_usd), float(price_brl)

    except Exception as e:
        print(f"⚠️ Erro ao buscar preço CMC: {e}")
        return None, None


def append_price_to_csv():
    """
    Adiciona o preço atual do BTC no CSV.
    """

    price_usd, price_brl = fetch_btc_price()

    if price_usd is None:
        return

    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "close": price_usd,
        "close_brl": price_brl
    }

    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_csv(CSV_PATH, index=False)

    print(
        f"✅ CSV atualizado | USD: {price_usd:.2f} | BRL: {price_brl:.2f} | {new_row['timestamp']}"
    )