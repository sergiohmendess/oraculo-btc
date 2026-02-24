# api/app.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from engine.model_loader import load_model
from engine.scenario_generator import generate_scenario
from engine.data_loader import load_data
import requests
import traceback
import time

app = FastAPI(title="Oráculo BTC", version="9.0-STABLE")

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
UPDATE_INTERVAL = 300  # 5 minutos (300s) para atualização automática

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
# PREÇO AO VIVO (YAHOO)
# =========================
def get_btc_prices():
    try:
        # USD Binance
        usd_res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT", timeout=5).json()
        if "price" not in usd_res:
            raise ValueError("Binance API error for BTCUSDT")
        price_usd = float(usd_res["price"])
        
        # BRL Binance
        brl_res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=BTCBRL", timeout=5).json()
        if "price" not in brl_res:
            raise ValueError("Binance API error for BTCBRL")
        price_brl = float(brl_res["price"])
        
        return price_usd, price_brl
    except Exception as e:
        print(f"❌ ERRO Binance: {e}")
        # Fallback Yahoo Finance
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            usd_data = requests.get(
                "https://query1.finance.yahoo.com/v7/finance/quote?symbols=BTC-USD",
                headers=headers, timeout=10
            ).json()
            price_usd = float(usd_data["quoteResponse"]["result"][0]["regularMarketPrice"])

            brl_data = requests.get(
                "https://query1.finance.yahoo.com/v7/finance/quote?symbols=BTC-BRL",
                headers=headers, timeout=10
            ).json()
            price_brl = float(brl_data["quoteResponse"]["result"][0]["regularMarketPrice"])

            return price_usd, price_brl
        except Exception:
            print("❌ ERRO DETALHADO YAHOO FALLBACK:")
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail="Erro ao buscar preços")

# =========================
# ROTA PRINCIPAL
# =========================
@app.get("/btc-scenario")
def btc_scenario():
    global cached_result, last_update_time

    if model is None:
        raise HTTPException(status_code=500, detail="Modelo não disponível")

    current_time = time.time()
    if cached_result and (current_time - last_update_time) < UPDATE_INTERVAL:
        return cached_result

    try:
        df = load_data()
        result = generate_scenario(df, model)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Dataset não encontrado.")
    except Exception:
        print("❌ ERRO INTERNO:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Erro interno no processamento")

    prob_up = result.get("prob_up", 0)
    prob_down = result.get("prob_down", 0)

    # Tentativa de pegar preços
    try:
        price_usd, price_brl = get_btc_prices()
    except HTTPException:
        price_usd, price_brl = 0.0, 0.0

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
        "timeframe": "5m",
        "last_update": int(time.time())
    }

    cached_result = json_result
    last_update_time = current_time

    return json_result

@app.get("/")
def root():
    return {"message": "🔮 Oráculo BTC API rodando - v9.0-STABLE"}