class Backtester:
    def __init__(self, scenarios):
        self.scenarios = scenarios

    def simple_strategy(self):
        atual = self.scenarios["atual"]
        previsto = self.scenarios["previsto"]

        if previsto > atual:
            return "📈 Comprar"
        elif previsto < atual:
            return "📉 Vender"
        else:
            return "➡ Manter"

    def report(self):
        return {
            "estrategia": self.simple_strategy(),
            "cenarios": self.scenarios
        }

