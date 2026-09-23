"""Tracing mínimo del agente.

Cada llamada a una función decorada con @traced debería dejar un span en SPANS:
    {"name": str, "duration_ms": float, "ok": bool, "error": str | None}
"""
import functools  # noqa: F401

SPANS: list[dict] = []


def traced(fn):
    return fn


def get_spans() -> list[dict]:
    return list(SPANS)


def reset() -> None:
    SPANS.clear()
