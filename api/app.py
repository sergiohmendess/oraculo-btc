# api/app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from engine.model_loader import load_model
from engine.scenario_generator import generate_scenario
from engine.data_loader import load_data
import requests
import traceback
import time


app = FastAPI(title="Oráculo BTC", version="7.2-CLOUD-COINGECKO")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

cached_result = None
last_update_time = 0

# Cache ultra curto apenas para evitar spam
UPDATE_INTERVAL = 5  # segundos


# =========================
# CARREGA MODELO
# =========================
try:
    model = load_model()
    print("✅ Modelo carregado com sucesso")
except Exception as e:
    print(f"❌ ERRO ao carregar modelo: {e}")
    traceback.print_exc()
    model = None


# =========================
# PREÇO AO VIVO (COINGECKO)
# =========================
def get_btc_prices():
    try:
        print("🔄 Buscando preços na CoinGecko...")

        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd,brl"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        price_usd = float(data["bitcoin"]["usd"])
        price_brl = float(data["bitcoin"]["brl"])

        return price_usd, price_brl

    except Exception:
        print("❌ ERRO DETALHADO COINGECKO:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Erro ao buscar preço da CoinGecko")


# =========================
# ROTA PRINCIPAL
# =========================
@app.get("/btc-scenario")
def get_btc_scenario():

    global cached_result, last_update_time

    if model is None:
        raise HTTPException(status_code=500, detail="Modelo não disponível")

    current_time = time.time()

    # Cache curto
    if cached_result and (current_time - last_update_time) < UPDATE_INTERVAL:
        return cached_result

    try:
        df = load_data()
        result = generate_scenario(df, model)

    except Exception:
        print("❌ ERRO INTERNO:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Erro interno no processamento")

    prob_up = result["prob_up"]
    prob_down = result["prob_down"]

    price_usd, price_brl = get_btc_prices()

    # Determinação da tendência
    if prob_up > prob_down:
        trend = "Tendência de Alta 📈"
    elif prob_down > prob_up:
        trend = "Tendência de Queda 📉"
    else:
        trend = "Tendência Estável ⚖️"

    json_result = {
        "price_usd": round(price_usd, 2),
        "price_brl": round(price_brl, 2),
        "prob_up": round(prob_up * 100, 2),
        "prob_down": round(prob_down * 100, 2),
        "confidence": round(abs(prob_up - prob_down) * 100, 2),
        "trend": trend,
        "timeframe": "15m",
        "last_update": int(time.time())
    }

    cached_result = json_result
    last_update_time = current_time

    return json_result


@app.get("/")
def root():
    return {
        "message": "🔮 Oráculo BTC API rodando - v7.2 Cloud CoinGecko"
    }