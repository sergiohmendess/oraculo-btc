# engine/model_loader.py

import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "modelo.pkl")

def save_model(model):
    joblib.dump(model, MODEL_PATH)
    print(f"[model_loader] Modelo salvo em: {MODEL_PATH}")

def load_model():
    from joblib import load

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Modelo não encontrado em: {MODEL_PATH}")

    print(f"[model_loader] Carregando modelo de: {MODEL_PATH}")
    return load(MODEL_PATH)