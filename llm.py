"""Cliente del LLM.

`client` es cualquier objeto con el método:
    client.complete(prompt: str, model: str, timeout: float | None = None) -> str
"""


def call_llm(client, prompt: str, model: str = "claude-sonnet") -> str:
    return client.complete(prompt, model=model)
