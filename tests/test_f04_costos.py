from agent.config import PRICES_USD_PER_MTOK as P
from agent.config import choose_model


def test_tareas_simples_usan_modelo_mas_barato():
    for simple in ("clasificar", "extraer"):
        assert P[choose_model(simple)] < P[choose_model("razonamiento_complejo")]


def test_modelos_validos():
    for t in ("clasificar", "extraer", "resumir", "planificar", "razonamiento_complejo"):
        assert choose_model(t) in P
