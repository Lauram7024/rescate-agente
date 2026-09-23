from agent.react import run_agent


class LoopLLM:
    """Un LLM que nunca decide terminar."""

    def __init__(self):
        self.calls = 0

    def next(self, messages):
        self.calls += 1
        if self.calls > 50:
            raise RuntimeError("loop infinito: el agente nunca se detuvo")
        return {"type": "tool", "name": "buscar_usuario", "args": {"user_id": 1}}


def test_agente_se_detiene_en_max_steps():
    llm = LoopLLM()
    out = run_agent("¿quién es el 1?", llm, max_steps=5)
    assert "answer" in out
    assert llm.calls <= 6


def test_tool_inexistente_no_revienta():
    class LLM:
        def __init__(self):
            self.n = 0

        def next(self, messages):
            self.n += 1
            if self.n == 1:
                return {"type": "tool", "name": "tool_que_no_existe", "args": {}}
            return {"type": "final", "content": "ok"}

    out = run_agent("hola", LLM())
    assert "answer" in out
