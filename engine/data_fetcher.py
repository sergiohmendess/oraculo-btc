import requests
import pandas as pd
import time
from datetime import datetime, timezone

BINANCE_URL = "https://api.binance.com/api/v3/klines"
SYMBOL = "BTCUSDT"
INTERVAL = "1d"
LIMIT = 1000  # Máximo permitido por requisição


def get_binance_klines(symbol=SYMBOL, interval=INTERVAL, start_time=None, end_time=None):
    """
    Baixa candles da Binance com paginação automática.
    Retorna DataFrame bruto.
    """

    all_data = []
    current_start = start_time
    max_loops = 100  # proteção contra loop infinito
    loop_count = 0

    while True:
        loop_count += 1
        if loop_count > max_loops:
            print("⚠ Loop máximo atingido. Interrompendo paginação.")
            break

        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": LIMIT
        }

        if current_start:
            params["startTime"] = current_start

        if end_time:
            params["endTime"] = end_time

        try:
            r = requests.get(BINANCE_URL, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print("❌ Erro ao buscar dados da Binance:", e)
            break

        if not data:
            break

        all_data.extend(data)

        last_close_time = data[-1][6]
        current_start = last_close_time + 1

        time.sleep(0.2)  # respeitar limite da API

    if not all_data:
        raise Exception("Nenhum dado retornado da Binance.")

    df = pd.DataFrame(all_data)
    return df


def clean_klines(df_raw):
    """
    Converte retorno bruto da Binance em DataFrame limpo e padronizado.
    """

    df = pd.DataFrame({
        "timestamp": df_raw[0].astype("int64"),
        "open": df_raw[1].astype(float),
        "high": df_raw[2].astype(float),
        "low": df_raw[3].astype(float),
        "close": df_raw[4].astype(float),
        "volume": df_raw[5].astype(float)
    })

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)

    df = df.drop_duplicates("timestamp")
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Remove último candle se ainda estiver incompleto
    now_utc = datetime.now(timezone.utc)
    last_timestamp = df["timestamp"].iloc[-1]

    if last_timestamp.date() == now_utc.date():
        print("⚠ Removendo último candle incompleto…")
        df = df.iloc[:-1]

    return df


def save_csv(df, path="data/btc_base.csv"):
    df.to_csv(path, index=False)
    print(f"✔ Dataset salvo em: {path}")


def fetch_and_update():
    print("📡 Baixando históricos da Binance…")

    start_timestamp = int(pd.Timestamp("2013-01-01", tz="UTC").timestamp() * 1000)

    df_raw = get_binance_klines(start_time=start_timestamp)
    df_clean = clean_klines(df_raw)
    save_csv(df_clean)

    print("✨ Base atualizada com sucesso!")


# Função usada pelo app.py
def update_csv():
    fetch_and_update()


if __name__ == "__main__":
    fetch_and_update()