"""Loop ReAct del agente.

`llm.next(messages)` devuelve una de dos acciones:
    {"type": "tool", "name": "<tool>", "args": {...}}
    {"type": "final", "content": "<respuesta>"}
"""
from agent.tools import TOOLS


def run_agent(query: str, llm, tools: dict | None = None, max_steps: int = 8) -> dict:
    tools = tools or TOOLS
    messages = [{"role": "user", "content": query}]
    while True:
        action = llm.next(messages)
        if action["type"] == "final":
            return {"answer": action["content"], "steps": len(messages)}
        fn = tools[action["name"]]
        result = fn(**action.get("args", {}))
        messages.append({"role": "tool", "name": action["name"], "content": result})
