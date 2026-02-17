import os
import joblib
from sklearn.ensemble import RandomForestClassifier

def train_model(df):
    df['future'] = df['close'].shift(-1)
    df['target'] = (df['future'] > df['close']).astype(int)
    df = df.dropna()

    X = df[['rsi14','sma20','ema20','ret']]
    y = df['target']

    model = RandomForestClassifier(
        n_estimators=600,
        max_depth=8,
        min_samples_split=5
    )
    model.fit(X, y)

    path = os.path.join(os.path.dirname(__file__), '..', 'model', 'modelo.pkl')
    joblib.dump(model, path)
    return model
