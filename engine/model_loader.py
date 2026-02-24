import joblib

MODEL_PATH = "model/modelo.pkl"

def load_model():
    return joblib.load(MODEL_PATH)