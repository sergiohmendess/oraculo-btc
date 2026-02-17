async function loadScenario() {
    const response = await fetch("../engine/output.json");
    const data = await response.json();

    document.getElementById("proba_up").innerText = (data.up_probability*100).toFixed(1)+"%";
    document.getElementById("proba_down").innerText = (data.down_probability*100).toFixed(1)+"%";
    document.getElementById("trend").innerText = data.trend;
    document.getElementById("risk").innerText = data.risk;
    document.getElementById("insights_text").innerText = data.insights;

    createChart(data.history);
}

function createChart(history) {
    const dates = history.map(x => x.timestamp);
    const prices = history.map(x => x.close);

    Plotly.newPlot("chart",
        [{
            x: dates,
            y: prices,
            type: "scatter",
            mode: "lines",
            line: { width: 2 }
        }],
        {
            paper_bgcolor: "#0d1117",
            plot_bgcolor: "#0d1117",
            font: { color: "#e6edf3" }
        }
    );
}

loadScenario();
