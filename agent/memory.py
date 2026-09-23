"""Memoria conversacional del agente."""


class Memory:
    def __init__(self, max_turns: int = 10):
        self.max_turns = max_turns
        self.turns: list[dict] = []

    def add(self, role: str, content: str) -> None:
        self.turns.append({"role": role, "content": content})

    def get_context(self) -> list[dict]:
        """Turnos que se envían al LLM en cada llamada."""
        return list(self.turns)
