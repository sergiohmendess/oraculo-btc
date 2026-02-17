# engine/cmc_price.py

import requests
import pandas as pd
import os
from datetime import datetime

# Coloque aqui sua API Key do CoinMarketCap
API_KEY = "9e63a969fe4d40528c3d4c7945050173"

# Caminho do CSV do projeto existente
CSV_PATH = os.path.join("data", "btc_base.csv")

def fetch_btc_price():
    """
    Pega o preço atual do BTC em USD usando CoinMarketCap API.
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    params = {
        "symbol": "BTC",
        "convert": "USD"
    }
    headers = {
        "X-CMC_PRO_API_KEY": API_KEY,
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        price = data["data"]["BTC"]["quote"]["USD"]["price"]
        return price
    except Exception as e:
        print(f"⚠️ Erro ao buscar preço CMC: {e}")
        return None

def append_price_to_csv():
    """
    Adiciona o preço atual do BTC no CSV, mantendo histórico.
    """
    price = fetch_btc_price()
    if price is None:
        return
    
    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "close": price
    }

    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_csv(CSV_PATH, index=False)
    print(f"✅ CSV atualizado com preço {price:.2f} USD em {new_row['timestamp']}")
