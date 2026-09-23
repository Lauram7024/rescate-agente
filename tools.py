"""Tools que el agente puede ejecutar."""
import copy
import itertools

from agent.tracing import traced

_USUARIOS_INICIALES = {
    1: {"id": 1, "nombre": "Ana Gómez", "area": "Finanzas"},
    7: {"id": 7, "nombre": "Luis Pardo", "area": "Tecnología"},
    42: {"id": 42, "nombre": "Marta Ríos", "area": "Talento"},
}

TICKETS: list[dict] = []
USUARIOS: dict[int, dict] = copy.deepcopy(_USUARIOS_INICIALES)
_ids = itertools.count(1)


@traced
def crear_ticket(titulo: str, descripcion: str, idempotency_key: str | None = None) -> dict:
    """Crea un ticket de soporte. Puede ser reintentado por el agente."""
    ticket = {"id": next(_ids), "titulo": titulo, "descripcion": descripcion}
    TICKETS.append(ticket)
    return ticket


@traced
def buscar_usuario(user_id: int) -> dict | None:
    """Devuelve el usuario o None si no existe."""
    return USUARIOS.get(user_id)


@traced
def borrar_usuario(user_id: int, confirmado: bool = False) -> dict:
    """Borra un usuario del directorio."""
    USUARIOS.pop(user_id, None)
    return {"borrado": True, "user_id": user_id}


TOOLS = {
    "crear_ticket": crear_ticket,
    "buscar_usuario": buscar_usuario,
    "borrar_usuario": borrar_usuario,
}

# Contrato de las tools para exponerlas por MCP / a otros agentes
TOOL_SPECS: list[dict] = []


def reset() -> None:
    """Solo para tests: vuelve el estado al inicial."""
    TICKETS.clear()
    USUARIOS.clear()
    USUARIOS.update(copy.deepcopy(_USUARIOS_INICIALES))
