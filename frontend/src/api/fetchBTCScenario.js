// frontend/src/api/fetchBTCScenario.js

// ==========================
// BACKEND LOCAL HARD-CODED
// ==========================
// Substituí a variável de ambiente para teste definitivo
const API_URL = "http://127.0.0.1:8000/btc-scenario";

const TIMEOUT = 7000; // 7 segundos

// ==========================
// FUNÇÃO AUXILIAR SEGURA
// ==========================
function toNumber(value, fallback = 0) {
  const n = Number(value);
  return Number.isFinite(n) ? n : fallback;
}

// ==========================
// FUNÇÃO PRINCIPAL
// ==========================
export async function fetchBTCScenario() {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT);

  try {
    const response = await fetch(API_URL, {
      method: "GET",
      headers: { Accept: "application/json" },
      signal: controller.signal
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`Erro HTTP ${response.status}`);
    }

    const data = await response.json();

    // ==========================
    // NORMALIZAÇÃO DEFINITIVA
    // ==========================
    const priceBRL = toNumber(data.price_brl);
    const priceUSD = toNumber(data.price_usd);
    const probUp = toNumber(data.prob_up);
    const probDown = toNumber(data.prob_down);
    const confidence =
      data.confidence !== undefined
        ? toNumber(data.confidence)
        : Math.abs(probUp - probDown);

    return {
      price_usd: priceUSD,
      price_brl: priceBRL,
      prob_up: probUp,
      prob_down: probDown,
      trend: data.trend || "Indefinida",
      timeframe: data.timeframe || "15m",
      confidence: confidence,
      last_update: data.last_update || null
    };
  } catch (error) {
    clearTimeout(timeoutId);

    console.error("Erro ao buscar cenário BTC:", error.message);

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