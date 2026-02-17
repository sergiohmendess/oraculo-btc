🔮 Oráculo BTC

Short-Term Statistical Model • 15 minutos

O Oráculo BTC é um sistema de análise estatística de curto prazo para o Bitcoin, capaz de calcular probabilidades de Alta e Queda com base em dados recentes do mercado.

🚀 Funcionalidades

📊 Modelo estatístico de previsão (15 minutos)

💰 Preço atual em USD (CoinMarketCap)

🇧🇷 Preço atual em BRL

📈 Probabilidade de Alta

📉 Probabilidade de Queda

🎯 Confiança Estatística

🧠 Tendência sugerida

⚡ Cache inteligente (reduz requisições externas)

🔄 Atualização automática de dados

🏗️ Arquitetura

Frontend:

React + Vite

Backend:

FastAPI

Modelo pré-treinado

Atualização via CoinMarketCap API

Sistema de cache em memória

Fluxo do Sistema:

Usuário → /btc-scenario → 
Cache verifica intervalo → 
Se necessário:
    - Atualiza preço (CMC)
    - Atualiza CSV
    - Carrega dados
    - Gera cenário
Retorna JSON final
🧠 Como Funciona o Modelo

Atualiza o preço do BTC via CoinMarketCap

Armazena os dados em CSV local

Carrega os dados históricos

Executa modelo estatístico

Calcula:

Probabilidade de Alta

Probabilidade de Queda

Determina Tendência com base na maior probabilidade

Calcula Confiança Estatística

Observação: A soma de Alta + Queda sempre = 100%.

📊 Confiança Estatística

Imagine uma balança:

Alta = 50% | Queda = 50% → Mercado indeciso

Alta = 60% | Queda = 40% → Existe vantagem real

Quanto maior a diferença entre as probabilidades, maior o desequilíbrio e mais forte o sinal.

🔐 Cache Inteligente

O backend possui um sistema de cache global.

Intervalo padrão:

UPDATE_INTERVAL = 180  # segundos

Isso garante:

Múltiplos usuários não geram múltiplas chamadas externas

A API externa é chamada no máximo 1 vez a cada 3 minutos

Redução drástica de requisições

📁 Estrutura do Projeto
oraculo-btc/
│
├── api/
│   └── app.py
│
├── engine/
│   ├── model_loader.py
│   ├── scenario_generator.py
│   ├── data_loader.py
│   └── update_btc.py
│
├── data/
│   └── btc_base.csv
│
├── src/          # Frontend React
│
├── requirements.txt
└── README.md
🛠️ Instalação Local
Backend

Criar ambiente virtual:

python -m venv venv

Ativar o ambiente:

Windows:

venv\Scripts\activate

Linux/Mac:

source venv/bin/activate

Instalar dependências:

pip install -r requirements.txt

Rodar API:

uvicorn api.app:app --reload

API disponível em:

http://127.0.0.1:8000
Frontend
npm install
npm run dev
🌐 Endpoint Principal

GET /btc-scenario

Retorno exemplo:

{
  "price_usd": 67827.94,
  "price_brl": 354192.00,
  "prob_up": 50.19,
  "prob_down": 49.81,
  "trend": "Tendência de Alta 📈",
  "timeframe": "15m"
}
⚠ Aviso Legal

Sistema voltado para análise estatística de curto prazo.
Não constitui recomendação financeira.

👨‍💻 Desenvolvedor

Sérgio Mendes