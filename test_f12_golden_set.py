import json
from pathlib import Path

from agent.router import VALID_ROUTES

GOLDEN = Path(__file__).resolve().parent.parent / "evals" / "golden_set.json"


def test_golden_set_suficiente_y_diverso():
    casos = json.loads(GOLDEN.read_text(encoding="utf-8"))
    assert len(casos) >= 8
    assert len({c["id"] for c in casos}) == len(casos), "ids repetidos"
    for c in casos:
        assert isinstance(c["input"], str) and c["input"].strip()
        assert c["expected_route"] in VALID_ROUTES
        assert c["categoria"] in ("normal", "borde", "adversarial")
    cats = [c["categoria"] for c in casos]
    assert cats.count("borde") >= 2, "faltan casos borde"
    assert cats.count("adversarial") >= 2, "faltan casos adversariales"
