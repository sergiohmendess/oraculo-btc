# api/app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from engine.model_loader import load_model
from engine.scenario_generator import generate_scenario
from engine.data_loader import load_data
from engine.update_btc import update_csv
import requests
import traceback
import time


app = FastAPI(title="Oráculo BTC", version="7.0-LIVE-BINANCE-PRO")

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
# PREÇO AO VIVO BINANCE (PRO)
# =========================
def get_btc_prices():
    try:
        # ===== BTCUSDT (USD)
        usd_response = requests.get(
            "https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT",
            timeout=3
        )
        usd_response.raise_for_status()
        usd_data = usd_response.json()

        usd_bid = float(usd_data["bidPrice"])
        usd_ask = float(usd_data["askPrice"])
        price_usd = (usd_bid + usd_ask) / 2


        # ===== BTCBRL (BRL REAL)
        brl_response = requests.get(
            "https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCBRL",
            timeout=3
        )
        brl_response.raise_for_status()
        brl_data = brl_response.json()

        brl_bid = float(brl_data["bidPrice"])
        brl_ask = float(brl_data["askPrice"])
        price_brl = (brl_bid + brl_ask) / 2

        return price_usd, price_brl

    except Exception as e:
        print("❌ Erro ao buscar preços Binance:", e)
        return 0.0, 0.0


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
        update_csv()
        df = load_data()
        result = generate_scenario(df, model)
    except Exception as e:
        print("Erro interno:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro interno")

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
        "message": "🔮 Oráculo BTC API rodando - v7.0 Live Binance PRO"
    }