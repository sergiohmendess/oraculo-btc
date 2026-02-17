from data_loader import load_raw_data
from feature_engineering import create_features

df = load_raw_data()
df = create_features(df)

print("\n📋 COLUNAS DO DATAFRAME APÓS FEATURE ENGINEERING:\n")
print(list(df.columns))

print("\n📊 PRIMEIRAS LINHAS:\n")
print(df.head())
