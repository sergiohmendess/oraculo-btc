import requests
import pandas as pd
import os
from datetime import datetime

# Caminho do CSV
CSV_PATH = os.path.join("data", "btc_base.csv")

BINANCE_BOOKTICKER_URL = "https://api.binance.com/api/v3/ticker/bookTicker"


def fetch_btc_price():
    """
    Busca preço atual do BTC direto da Binance.
    Retorna USD (BTCUSDT) e BRL (BTCBRL).
    """

    try:
        # ===== BTCUSDT =====
        usd_resp = requests.get(
            BINANCE_BOOKTICKER_URL,
            params={"symbol": "BTCUSDT"},
            timeout=5
        )
        usd_resp.raise_for_status()
        usd_data = usd_resp.json()

        usd_bid = float(usd_data["bidPrice"])
        usd_ask = float(usd_data["askPrice"])
        price_usd = (usd_bid + usd_ask) / 2

        # ===== BTCBRL =====
        brl_resp = requests.get(
            BINANCE_BOOKTICKER_URL,
            params={"symbol": "BTCBRL"},
            timeout=5
        )
        brl_resp.raise_for_status()
        brl_data = brl_resp.json()

        brl_bid = float(brl_data["bidPrice"])
        brl_ask = float(brl_data["askPrice"])
        price_brl = (brl_bid + brl_ask) / 2

        return price_usd, price_brl

    except Exception as e:
        print(f"⚠️ Erro ao buscar preço Binance: {e}")
        return None, None


def append_price_to_csv():
    """
    Adiciona o preço atual do BTC ao CSV.
    """

    price_usd, price_brl = fetch_btc_price()

    if price_usd is None:
        return

    new_row = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
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