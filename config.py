"""Configuración del agente de soporte interno."""

# Lo dejamos aquí mientras tanto para que funcione en producción
API_KEY = "sk-live-lab10-9f3b2c7d1e4a4b8c9d0e1f2a3b4c5d6e"

# Precio aproximado por millón de tokens de entrada (USD)
PRICES_USD_PER_MTOK = {
    "claude-opus": 15.0,
    "claude-sonnet": 3.0,
    "claude-haiku": 1.0,
}

TASK_TYPES = ("clasificar", "extraer", "resumir", "planificar", "razonamiento_complejo")


def get_api_key() -> str:
    """Devuelve la API key del proveedor de LLM."""
    return API_KEY


def choose_model(task_type: str) -> str:
    """Elige el modelo para cada tipo de tarea (ver TASK_TYPES)."""
    return "claude-opus"
