import { useEffect, useState, useRef } from "react";
import { fetchBTCScenario } from "./api/fetchBTCScenario";
import "./App.css";

function App() {
  const [btcData, setBtcData] = useState({
    price_usd: 0,
    price_brl: 0,
    prob_up: 0,
    prob_down: 0,
    trend: "",
    timeframe: "15m"
  });

  const [lastUpdate, setLastUpdate] = useState(null);
  const chartRef = useRef(null);

  const REFRESH_INTERVAL = 210000;

  /* =========================
     BUSCA DE DADOS
  ========================== */
  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchBTCScenario();

        setBtcData({
          price_usd: Number(data.price_usd),
          price_brl: Number(data.price_brl),
          prob_up: Number(data.prob_up),
          prob_down: Number(data.prob_down),
          trend: data.trend,
          timeframe: data.timeframe || "15m"
        });

        setLastUpdate(new Date());
      } catch (error) {
        console.error("Erro ao buscar dados:", error);
      }
    }

    loadData();
    const interval = setInterval(loadData, REFRESH_INTERVAL);
    return () => clearInterval(interval);
  }, []);

  /* =========================
     TRADINGVIEW
  ========================== */
  useEffect(() => {
    if (!window.TradingView) {
      const script = document.createElement("script");
      script.src = "https://s3.tradingview.com/tv.js";
      script.async = true;
      script.onload = createWidget;
      document.body.appendChild(script);
    } else {
      createWidget();
    }

    function createWidget() {
      if (!window.TradingView || !chartRef.current) return;

      chartRef.current.innerHTML = "";

      new window.TradingView.widget({
        autosize: true,
        symbol: "COINBASE:BTCUSD",
        interval: btcData.timeframe.replace("m", ""),
        timezone: "Etc/UTC",
        theme: "dark",
        style: "1",
        locale: "pt",
        toolbar_bg: "#0b0f1a",
        enable_publishing: false,
        hide_side_toolbar: false,
        container_id: "tradingview_chart"
      });
    }

  }, [btcData.timeframe]);

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  /* =========================
     CONFIANÇA
  ========================== */
  const confidence = Math.abs(
    btcData.prob_up - btcData.prob_down
  );

  const getConfidenceLabel = () => {
    if (confidence <= 5) return "Mercado Indeciso ⚖️";
    if (confidence <= 15) return "Leve Vantagem 📊";
    if (confidence <= 30) return "Vantagem Moderada 📈";
    return "Forte Pressão 🔥";
  };

  return (
    <div className="page-wrapper">
      <div className="app-container">

        <h1 className="title">🔮 ORÁCULO BTC</h1>


        <div className="card">

          {/* PREÇO USD */}
          <div className="card-item">
            <span className="label">Preço Atual (USD):</span>
            <span className="value">
              ${btcData.price_usd.toLocaleString("en-US", { minimumFractionDigits: 2 })}
            </span>
          </div>

          {/* PREÇO BRL */}
          <div className="card-item">
            <span className="label">Preço Atual (BRL):</span>
            <span className="value">
              R$ {btcData.price_brl.toLocaleString("pt-BR", { minimumFractionDigits: 2 })}
            </span>
          </div>

          <div className="card-item">
            <span className="label">Probabilidade de Alta:</span>
            <span className="value prob-up">
              {btcData.prob_up.toFixed(2)}%
            </span>
          </div>

          <div className="card-item">
            <span className="label">Probabilidade de Queda:</span>
            <span className="value prob-down">
              {btcData.prob_down.toFixed(2)}%
            </span>
          </div>

          {/* BARRA PROBABILIDADE */}
          <div className="prob-bar-wrapper">
            <div
              className="prob-bar-up"
              style={{ width: `${btcData.prob_up}%` }}
            />
            <div
              className="prob-bar-down"
              style={{ width: `${btcData.prob_down}%` }}
            />
          </div>

<div className="card-item trend">
  <span className="label">Tendência&nbsp;:</span>
  <span className="value trend-value">
    &nbsp;{btcData.trend}
  </span>
</div>


          {/* CONFIANÇA VISUAL */}
          <div className="confidence-box">

            <div>
              🎯 Confiança Estatística: {confidence.toFixed(2)}%
            </div>

            <div className="confidence-bar-wrapper">
              <div
                className="confidence-bar"
                style={{ width: `${confidence}%` }}
              />
            </div>

            <div className="confidence-label">
              {getConfidenceLabel()}
            </div>

            <small>
              Quanto maior a diferença entre Alta e Queda,
              maior o desequilíbrio do mercado.
            </small>

          </div>

          {lastUpdate && (
            <div className="last-update">
              Atualizado às {lastUpdate.toLocaleTimeString()}
            </div>
          )}

        </div>

        {/* GRÁFICO */}
        <div className="chart-container">
          <div
            id="tradingview_chart"
            ref={chartRef}
            style={{ width: "100%", height: "100%" }}
          />
        </div>

        {/* COMO FUNCIONA */}
        <div className="info-box">

          <h2>📊 Como Funciona?</h2>

          <p className="highlight">
            O Oráculo BTC analisa dados recentes do mercado e calcula
            probabilidades para os próximos {btcData.timeframe}.
          </p>

          <ul className="metrics-list">

            <li>
              <strong>💰 Preço Atual</strong><br/>
              Valor real do Bitcoin neste momento.
            </li>

            <li>
              <strong>📈 Probabilidade de Alta</strong><br/>
              Chance estimada do preço subir no curto prazo.
            </li>

            <li>
              <strong>📉 Probabilidade de Queda</strong><br/>
              Chance estimada do preço cair.
              Sempre soma 100% junto com a Alta.
            </li>

            <li>
              <strong>🎯 Confiança Estatística</strong><br/>
              Imagine uma balança:
              <br/>
              Se Alta = 50% e Queda = 50% → Mercado indeciso.
              <br/>
              Se Alta = 60% e Queda = 40% → Existe vantagem real.
              <br/><br/>
              A confiança mede o quanto essa balança está inclinada.
              Quanto maior a inclinação, mais forte o sinal.
            </li>

            <li>
              <strong>🧠 Tendência</strong><br/>
              Direção predominante sugerida pelo modelo
              com base nos dados recentes.
            </li>

          </ul>

          <div className="disclaimer">
            ⚠ Sistema voltado para análise estatística de curto prazo.
            Não constitui recomendação financeira.
          </div>

        </div>

        {/* FOOTER */}
        <footer className="footer">

          <p>Desenvolvido por <strong>Sérgio Mendes</strong></p>

          <div className="wallet">
            <p>⚡ Carteira Lightning:</p>
            <div className="wallet-box">
              <span>harmfulcreator83@walletofsatoshi.com</span>
              <button onClick={() =>
                copyToClipboard("harmfulcreator83@walletofsatoshi.com")
              }>
                Copiar
              </button>
            </div>
          </div>

          <div className="wallet">
            <p>⛓ Carteira On-Chain:</p>
            <div className="wallet-box">
              <span>bc1qf4pnt8hy0kt34xwdgg9tl3vgp0uh48ke5jru0u</span>
              <button onClick={() =>
                copyToClipboard("bc1qf4pnt8hy0kt34xwdgg9tl3vgp0uh48ke5jru0u")
              }>
                Copiar
              </button>
            </div>
          </div>

        </footer>

      </div>
    </div>
  );
}

export default App;
