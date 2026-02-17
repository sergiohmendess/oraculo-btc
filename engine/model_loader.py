import joblib
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'modelo.pkl')

def save_model(model):
    joblib.dump(model, MODEL_PATH)
    print(f'[model_loader] Modelo salvo em: {MODEL_PATH}')

def load_model():
    from joblib import load
    return load(MODEL_PATH)
