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

app = FastAPI(title="Oráculo BTC", version="3.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
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
# FUNÇÃO AUXILIAR PARA PEGAR BRL
# =========================
def get_btc_brl_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "brl"
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        return float(data["bitcoin"]["brl"])
    except Exception as e:
        print("⚠ Erro ao buscar preço BRL:", e)
        return 0


# =========================
# ROTA PRINCIPAL
# =========================
@app.get("/btc-scenario")
def get_btc_scenario():

    global cached_result, last_update_time

    if model is None:
        raise HTTPException(status_code=500, detail="Modelo não está disponível")

    current_time = time.time()

    # 🔥 Se ainda estiver dentro do intervalo, retorna cache
    if cached_result and (current_time - last_update_time) < UPDATE_INTERVAL:
        print("⚡ Retornando resultado em cache")
        return cached_result

    print("🔄 Atualizando cenário BTC...")

    # Atualiza CSV
    try:
        update_csv()
    except Exception as e:
        print(f"❌ ERRO ao atualizar CSV: {e}")
        traceback.print_exc()

    # Carrega dados
    try:
        df = load_data()
        if df.empty:
            raise ValueError("DataFrame vazio ao carregar dados BTC")
    except Exception as e:
        print(f"❌ ERRO ao carregar dados: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro ao carregar dados")

    # Gera cenário
    try:
        result = generate_scenario(df, model)
    except Exception as e:
        print(f"❌ ERRO ao gerar cenário: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Erro ao gerar cenário")

    prob_up = result["prob_up"]
    prob_down = result["prob_down"]
    price_usd = result["close"]

    # Busca preço BRL real
    price_brl = get_btc_brl_price()

    # Tendência
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

    # 🔥 Atualiza cache
    cached_result = json_result
    last_update_time = current_time

    print("🔮 Oráculo BTC enviando:", json_result)

    return json_result


@app.get("/")
def root():
    return {"message": "🔮 Oráculo BTC API rodando. Use /btc-scenario"}
