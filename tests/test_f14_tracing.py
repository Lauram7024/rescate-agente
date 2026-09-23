import pytest

from agent import tools, tracing


def test_cada_tool_deja_un_span():
    tracing.reset()
    tools.reset()
    tools.buscar_usuario(1)
    spans = [s for s in tracing.get_spans() if s.get("name") == "buscar_usuario"]
    assert spans, "no se registró ningún span"
    s = spans[-1]
    assert isinstance(s["duration_ms"], (int, float)) and s["duration_ms"] >= 0
    assert s["ok"] is True


def test_los_errores_quedan_trazados():
    tracing.reset()

    @tracing.traced
    def falla():
        raise ValueError("boom")

    with pytest.raises(ValueError):
        falla()
    s = tracing.get_spans()[-1]
    assert s["ok"] is False and "boom" in (s.get("error") or "")
