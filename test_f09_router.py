from agent.router import route

CASOS = [
    ("Crea un ticket porque no me funciona la VPN", "tickets"),
    ("NECESITO ABRIR UN TICKET YA", "tickets"),
    ("Borra al usuario 42", "usuarios"),
    ("¿En qué área está el Usuario 7?", "usuarios"),
    ("¿Cuántos días de vacaciones tengo?", "rag"),
]


def test_router():
    for query, esperado in CASOS:
        assert route(query) == esperado, f"{query!r} -> {route(query)!r}, esperaba {esperado!r}"
