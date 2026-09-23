from agent.memory import Memory


def test_memoria_acotada_y_con_lo_mas_reciente():
    m = Memory(max_turns=10)
    for i in range(100):
        m.add("user", f"msg {i}")
    ctx = m.get_context()
    assert len(ctx) <= 10
    assert ctx[-1]["content"] == "msg 99"


def test_respeta_otro_limite():
    m = Memory(max_turns=4)
    for i in range(20):
        m.add("user", f"msg {i}")
    assert len(m.get_context()) <= 4
