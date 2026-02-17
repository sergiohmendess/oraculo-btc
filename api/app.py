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

app = FastAPI(title="Oráculo BTC", version="3.4")

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

# =========================
# CACHE GLOBAL
# =========================
cached_result = None
last_update_time = 0
UPDATE_INTERVAL = 180  # 3 minutos

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
# FUNÇÃO PARA PEGAR USD E BRL (CMC)
# =========================
def get_btc_prices():

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    params = {
        "symbol": "BTC",
        "convert": "USD,BRL"
    }

    headers = {
        "X-CMC_PRO_API_KEY": "9e63a969fe4d40528c3d4c7945050173",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        print("STATUS CMC:", response.status_code)
        print("RESPOSTA CMC:", response.text)

        response.raise_for_status()

        data = response.json()

        price_usd = data["data"]["BTC"]["quote"]["USD"]["price"]
        price_brl = data["data"]["BTC"]["quote"]["BRL"]["price"]

        return float(price_usd), float(price_brl)

    except Exception as e:
        print("Erro ao buscar preços:", e)
        return 0, 0


# =========================
# ROTA PRINCIPAL
# =========================
@app.get("/btc-scenario")
def get_btc_scenario():

    global cached_result, last_update_time

    if model is None:
        raise HTTPException(status_code=500, detail="Modelo não está disponível")

    current_time = time.time()

    # Usa cache se estiver dentro do intervalo
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
        "trend": trend,
        "timeframe": "15m"
    }

    cached_result = json_result
    last_update_time = current_time

    return json_result


@app.get("/")
def root():
    return {"message": "🔮 Oráculo BTC API rodando. Use /btc-scenario"}
