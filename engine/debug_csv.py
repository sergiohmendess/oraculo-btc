import os
import pandas as pd

csv_path = r"C:\Users\sergi\OneDrive\Desktop\cenario-btc\engine\data\btc_base.csv"

print("🔍 Verificando CSV...")
print("📁 Existe?", os.path.exists(csv_path))

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    print("\n📊 PRIMEIRAS LINHAS:")
    print(df.head())

    print("\n📏 FORMATO DO DF:", df.shape)
else:
    print(f"❌ Arquivo NÃO encontrado: {csv_path}")
