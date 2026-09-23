import importlib
import re
from pathlib import Path

AGENT_DIR = Path(__file__).resolve().parent.parent / "agent"
PATRON = re.compile(r"sk-[A-Za-z0-9-]{20,}")


def test_no_hay_llaves_en_el_codigo():
    for f in AGENT_DIR.rglob("*.py"):
        assert not PATRON.search(f.read_text(encoding="utf-8")), f"Llave expuesta en {f.name}"


def test_llave_viene_del_entorno(monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "llave-de-prueba-123")
    from agent import config
    importlib.reload(config)
    assert config.get_api_key() == "llave-de-prueba-123"
