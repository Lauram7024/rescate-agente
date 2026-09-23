import re
from pathlib import Path

PROMPT = Path(__file__).resolve().parent.parent / "evals" / "judge_prompt.md"


def test_prompt_del_juez_es_evaluable():
    p = PROMPT.read_text(encoding="utf-8")
    for var in ("{pregunta}", "{respuesta}", "{referencia}"):
        assert var in p, f"falta la variable {var}"
    assert re.search(r"1\s*(a|al|-|–|y)\s*5", p), "falta una escala de 1 a 5"
    assert "json" in p.lower(), "debe pedir salida en JSON"
    assert "justific" in p.lower(), "debe pedir una justificación"
