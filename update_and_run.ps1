# Navega até a pasta engine
Set-Location -Path ".\engine"

# Atualiza CSV com cache (chama Python)
python .\update_btc.py

# Roda o main.py para gerar cenários
python .\main.py

# Mensagem final
Write-Host "✅ Sistema atualizado e cenário gerado com sucesso!"
