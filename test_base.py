"""Comportamiento que YA funciona. Si lo rompes, pierdes puntos."""
from agent import rag, router, tools
from agent.llm import call_llm
from agent.memory import Memory
from agent.react import run_agent


class OkClient:
    def complete(self, prompt, model=None, **kw):
        return "respuesta"


class ScriptedLLM:
    def __init__(self, actions):
        self.actions = list(actions)

    def next(self, messages):
        return self.actions.pop(0)


def test_crear_ticket_devuelve_id():
    tools.reset()
    t = tools.crear_ticket("VPN", "no conecta")
    assert "id" in t and t["titulo"] == "VPN"


def test_buscar_usuario():
    tools.reset()
    assert tools.buscar_usuario(7)["nombre"] == "Luis Pardo"
    assert tools.buscar_usuario(999) is None


def test_router_devuelve_ruta_valida():
    assert router.route("hola") in router.VALID_ROUTES


def test_retrieve_devuelve_lista_con_texto():
    res = rag.retrieve("vacaciones")
    assert isinstance(res, list) and res and "text" in res[0]


def test_call_llm_basico():
    assert call_llm(OkClient(), "hola") == "respuesta"


def test_agente_responde_directo():
    out = run_agent("hola", ScriptedLLM([{"type": "final", "content": "listo"}]))
    assert out["answer"] == "listo"


def test_agente_usa_tool_y_responde():
    tools.reset()
    llm = ScriptedLLM([
        {"type": "tool", "name": "buscar_usuario", "args": {"user_id": 1}},
        {"type": "final", "content": "Ana"},
    ])
    assert run_agent("¿quién es el 1?", llm)["answer"] == "Ana"


def test_memoria_guarda_turnos():
    m = Memory()
    m.add("user", "hola")
    assert m.get_context()[-1]["content"] == "hola"
