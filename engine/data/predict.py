import pandas as pd
import requests
import pickle
from datetime import datetime, timezone
from feature_engineering import prepare_features

BINANCE_URL = "https://api.binance.com/api/v3/ticker/price"
SYMBOL = "BTCUSDT"


def get_preco_atual():
    r = requests.get(BINANCE_URL, params={"symbol": SYMBOL})
    return float(r.json()["price"])


def load_model(path="model/modelo.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)


def gerar_previsao(df_base, model):
    preco_atual = get_preco_atual()

    # Substituir último close pelo preço atual
    df = df_base.copy()
    df.loc[df.index[-1], "close"] = preco_atual

    df = prepare_features(df)

    features = ["retorno", "rsi_14", "mm9", "mm21",
                "vol_7d", "vol_medio_7d", "dist_media"]

    X = df[features].iloc[-1:]

    prob = model.predict_proba(X)[0]

    return {
        "preco_atual": preco_atual,
        "probabilidade_alta": float(prob[1]),
        "probabilidade_queda": float(prob[0])
    }
