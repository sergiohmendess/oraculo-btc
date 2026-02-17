import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
from feature_engineering import create_features
import os

DATA_PATH = "data/btc_base.csv"
MODEL_PATH = "../model/modelo.pkl"

def train_model():
    print("📚 Carregando base...")
    df = pd.read_csv(DATA_PATH)

    print("🧪 Criando features...")
    df = create_features(df)

    df = df.dropna()

    # REMOVE qualquer coluna que não seja numérica
    df = df.select_dtypes(include=["float64", "int64"])

    # target precisa ser separado (pode ser removido ao filtrar)
    y = df["target"]
    X = df.drop("target", axis=1)

    print(f"🔢 Linhas após limpeza: {len(df)}")
    print(f"📌 Features usadas: {list(X.columns)}")

    # Split temporal (80/20)
    split_index = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_index], X.iloc[split_index:]
    y_train, y_test = y.iloc[:split_index], y.iloc[split_index:]

    print("🤖 Treinando modelo Logistic Regression...")
    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"🎯 Acurácia no teste: {acc:.4f}")

    os.makedirs("../model", exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"💾 Modelo salvo em: {MODEL_PATH}")

    return acc


if __name__ == "__main__":
    print("🚀 Iniciando treinamento...")
    train_model()
    print("✅ Treinamento concluído!")
