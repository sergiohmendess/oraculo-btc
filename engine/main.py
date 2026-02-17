# engine/main.py

from engine.data_loader import load_data
from engine.model_loader import save_model, load_model
from engine.trainer import train_model
from engine.scenario_generator import generate_scenario, print_scenario
from engine.cmc_price import append_price_to_csv


def run():
    print("🚀 Iniciando execução do cenário BTC...\n")

    # 1️⃣ Atualiza CSV com preço real
    try:
        append_price_to_csv()
        print("✅ Preço atualizado com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao atualizar preço: {e}\n")

    # 2️⃣ Carrega dados
    try:
        df = load_data()
        if df.empty:
            raise ValueError("DataFrame está vazio.")
        print("✅ Dados carregados com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return

    # 3️⃣ Carrega ou treina modelo
    try:
        model = load_model()
        print("✅ Modelo carregado com sucesso!\n")
    except Exception:
        print("⚠️ Modelo não encontrado. Treinando novo modelo...\n")
        model = train_model(df)
        save_model(model)
        print("✅ Modelo treinado e salvo com sucesso!\n")

    # 4️⃣ Gera cenário
    try:
        result = generate_scenario(df, model)
        print_scenario(result)
    except Exception as e:
        print(f"❌ Erro ao gerar cenário: {e}")


if __name__ == "__main__":
    run()