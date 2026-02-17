// frontend/src/api/fetchBTCScenario.js

const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const API_URL = `${BASE_URL}/btc-scenario`;

const TIMEOUT = 7000; // 7 segundos (mais seguro para produção)

/* =========================
   FUNÇÃO PRINCIPAL
========================= */
export async function fetchBTCScenario() {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT);

  try {
    const response = await fetch(API_URL, {
      method: "GET",
      headers: {
        "Accept": "application/json"
      },
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`Erro HTTP ${response.status}`);
    }

    const data = await response.json();

    /* =========================
       NORMALIZAÇÃO ROBUSTA
    ========================== */

    const priceUSD =
      data.price_usd !== undefined
        ? Number(data.price_usd)
        : Number(data.price);

    const priceBRL =
      data.price_brl !== undefined
        ? Number(data.price_brl)
        : 0;

    const probUp = Number(data.prob_up) || 0;
    const probDown = Number(data.prob_down) || 0;

    const confidence =
      data.confidence !== undefined
        ? Number(data.confidence)
        : Math.abs(probUp - probDown);

    return {
      price_usd: isFinite(priceUSD) ? priceUSD : 0,
      price_brl: isFinite(priceBRL) ? priceBRL : 0,
      prob_up: isFinite(probUp) ? probUp : 0,
      prob_down: isFinite(probDown) ? probDown : 0,
      trend: data.trend || "Indefinida",
      timeframe: data.timeframe || "15m",
      confidence: isFinite(confidence) ? confidence : 0,
      last_update: data.last_update || null
    };

  } catch (error) {
    clearTimeout(timeoutId);

    console.error("Erro ao buscar cenário BTC:", error.message);

    /* =========================
       FALLBACK SEGURO
    ========================== */

    return {
      price_usd: 0,
      price_brl: 0,
      prob_up: 0,
      prob_down: 0,
      trend: "Erro de conexão",
      timeframe: "-",
      confidence: 0,
      last_update: null
    };
  }
}
