# engine/scenario_generator.py

from engine.feature_engineering import create_features
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


def generate_scenario(df, model):
    """
    Gera cenário BTC usando indicadores técnicos + modelo treinado.
    Retorna probabilidades em formato decimal (0.53 e NÃO 53).
    """

    required_cols = ['rsi14', 'sma20', 'ema20', 'ret']
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        df = create_features(df)

    df = df.dropna()

    latest_row = df.iloc[-1:]
    X = latest_row[required_cols].values

    probs = model.predict_proba(X)[0]

    prob_up = float(probs[1])     # NÃO multiplicar aqui
    prob_down = float(probs[0])   # NÃO multiplicar aqui
    close_price = float(latest_row['close'].values[0])

    result = {
        "close": round(close_price, 2),
        "prob_up": prob_up,
        "prob_down": prob_down
    }

    return result


def print_scenario(result):
    """
    Exibe resultado no terminal (modo CLI).
    Aqui sim convertemos para porcentagem apenas para exibição.
    """

    prob_up = result['prob_up'] * 100
    prob_down = result['prob_down'] * 100

    trend = (
        "Tendência de Alta 📈"
        if prob_up > prob_down
        else "Tendência de Queda 📉"
        if prob_down > prob_up
        else "Tendência Estável ⚖️"
    )

    print("\n📊 Resultado do Oráculo BTC:")
    print(f"💹 Preço atual: ${result['close']:,.2f}")
    print(f"🔼 Probabilidade de subir: {prob_up:.2f}%")
    print(f"🔽 Probabilidade de cair: {prob_down:.2f}%")
    print(f"📌 Tendência sugerida: {trend}\n")