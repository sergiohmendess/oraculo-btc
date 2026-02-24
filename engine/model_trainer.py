import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from engine.feature_engineering import create_features
from engine.data_loader import load_data

MODEL_PATH = "model/modelo.pkl"

def train_model():
    df = load_data()
    df, features = create_features(df)

    X = df[features]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = GradientBoostingClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=3,
        random_state=42
    )

    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print(f"📊 Acurácia temporal: {acc:.4f}")

    joblib.dump({
        "model": model,
        "features": features
    }, MODEL_PATH)

    print("✅ Modelo salvo.")

if __name__ == "__main__":
    train_model()