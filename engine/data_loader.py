import pandas as pd
from pathlib import Path

# Caminho absoluto baseado na raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "btc_base.csv"

def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset não encontrado em {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # Garantir nomes corretos
    df.columns = [c.lower() for c in df.columns]

    return df