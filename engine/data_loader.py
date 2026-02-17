import pandas as pd

def load_data():
    file_path = "data/btc_base.csv"
    print(f"[data_loader] Carregando: {file_path}")

    df = pd.read_csv(file_path)

    print(f"[data_loader] Linhas carregadas: {len(df)}")

    # Converter timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Ordenar por data
    df = df.sort_values("timestamp")

    # Criar alvo (1 se subir, 0 se cair)
    df["target"] = (df["close"].shift(-1) > df["close"]).astype(int)

    # Remover última linha (sem target)
    df = df.dropna()

    return df