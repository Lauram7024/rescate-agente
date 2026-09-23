"""Router: decide qué sub-agente atiende la consulta."""

VALID_ROUTES = ("rag", "tickets", "usuarios")


def route(query: str) -> str:
    if "Ticket" in query:
        return "tickets"
    if "usuario" in query:
        return "usuarios"
    return "rag"
