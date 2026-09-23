import time

import pytest

from agent.llm import call_llm


class FlakyClient:
    def __init__(self, fallas):
        self.fallas = fallas
        self.calls = []

    def complete(self, prompt, model=None, **kw):
        self.calls.append(kw)
        if len(self.calls) <= self.fallas:
            raise TimeoutError("el proveedor no respondió")
        return "ok"


@pytest.fixture(autouse=True)
def sin_esperas(monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda s: None)


def test_reintenta_fallas_transitorias():
    c = FlakyClient(fallas=2)
    assert call_llm(c, "hola") == "ok"
    assert len(c.calls) == 3


def test_siempre_pasa_timeout():
    c = FlakyClient(fallas=0)
    call_llm(c, "hola")
    t = c.calls[0].get("timeout")
    assert t is not None and 0 < t <= 60


def test_no_reintenta_para_siempre():
    c = FlakyClient(fallas=1000)
    with pytest.raises(Exception):
        call_llm(c, "hola")
    assert len(c.calls) <= 5
