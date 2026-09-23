from agent import tools


def test_no_borra_sin_confirmacion():
    tools.reset()
    tools.borrar_usuario(42)
    assert tools.buscar_usuario(42) is not None


def test_borra_con_confirmacion():
    tools.reset()
    tools.borrar_usuario(42, confirmado=True)
    assert tools.buscar_usuario(42) is None
