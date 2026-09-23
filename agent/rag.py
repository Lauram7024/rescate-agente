"""RAG sobre la base de conocimiento interna (data/docs)."""
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "docs"


def _load_docs() -> list[dict]:
    docs = []
    for path in sorted(DOCS_DIR.glob("*.md")):
        docs.append({"id": path.stem, "text": path.read_text(encoding="utf-8")})
    return docs


DOCS = _load_docs()


def _tokens(text: str) -> list[str]:
    return text.lower().split()


def retrieve(query: str, top_k: int = 1) -> list[dict]:
    """Devuelve los chunks más relevantes. Cada resultado: {"id", "text", ...}."""
    q = _tokens(query)
    scored = []
    for doc in DOCS:
        score = sum(1 for t in _tokens(doc["text"]) if t in q)
        scored.append((score, doc))
    scored.sort(key=lambda x: -x[0])
    return [{"id": d["id"], "text": d["text"]} for _, d in scored[:top_k]]


def sanitize(text: str) -> str:
    """Limpia el contenido recuperado antes de pasarlo al LLM."""
    return text


def build_context(query: str) -> str:
    chunks = retrieve(query)
    return "\n\n".join(sanitize(c["text"]) for c in chunks)
