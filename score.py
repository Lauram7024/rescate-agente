#!/usr/bin/env python3
"""Calcula el puntaje del equipo. Uso:

    python score.py                 # resumen legible
    python score.py --json          # para el leaderboard
    python score.py --markdown      # para GitHub Actions
    python score.py --base <ref>    # rama/commit de referencia (default: origin/main o main)
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent

FALLAS = {
    "F01": ("Ingeniería híbrida", "Brief antes de tocar código", 5, 0),
    "F02": ("LLMOps", "Secretos fuera del código", 10, 5),
    "F03": ("LLMOps", "Resiliencia: timeout y reintentos acotados", 10, 0),
    "F04": ("LLMOps", "Costos: modelo según la tarea", 10, 0),
    "F05": ("Tools robustas", "Idempotencia en crear_ticket", 10, 0),
    "F06": ("Tools robustas", "Confirmación en efectos destructivos", 10, 5),
    "F07": ("Tools robustas", "Prompt injection en contenido recuperado", 10, 5),
    "F08": ("Arquitecturas", "ReAct: límite de pasos y tool inexistente", 10, 0),
    "F09": ("Arquitecturas", "Router", 10, 0),
    "F10": ("RAG", "Retrieval de calidad y fuentes para citar", 10, 0),
    "F11": ("Memoria", "Memoria acotada", 10, 0),
    "F12": ("Evaluación", "Golden set suficiente y diverso", 10, 0),
    "F13": ("Evaluación", "Prompt de LLM-as-judge evaluable", 10, 0),
    "F14": ("Observabilidad", "Tracing de tools y errores", 10, 0),
    "F15": ("Orquestación", "Contrato tipo MCP para las tools", 10, 0),
    "F16": ("Cloud", "Dockerfile listo para desplegar", 10, 0),
}
PUNTOS_AUDITORIA = 3
PALABRAS_MIN_AUDITORIA = 30
PENALIDAD_BASE = 5
PENALIDAD_MAX = 20
LINEAS_MIN_BRIEF = 5


def git(*args):
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def correr_tests():
    """Devuelve {archivo: [True/False por test]}."""
    with tempfile.TemporaryDirectory() as tmp:
        xml = Path(tmp) / "r.xml"
        try:
            subprocess.run(
                [sys.executable, "-m", "pytest", "-q", f"--junitxml={xml}"],
                cwd=ROOT, capture_output=True, text=True, timeout=180,
            )
        except subprocess.TimeoutExpired:
            return {}
        if not xml.exists():
            return {}
        resultados = {}
        for tc in ET.parse(xml).getroot().iter("testcase"):
            etiqueta = f"{tc.get('classname', '')} {tc.get('name', '')}"
            m = re.search(r"test_(f\d{2}|base)", etiqueta)
            if not m:
                continue
            clave = m.group(1).upper() if m.group(1) != "base" else "BASE"
            ok = not any(tc.find(t) is not None for t in ("failure", "error", "skipped"))
            resultados.setdefault(clave, []).append(ok)
        return resultados


def brief(base):
    path = ROOT / "BRIEF.md"
    texto = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S) if path.exists() else ""
    lineas = [l for l in texto.splitlines() if l.strip() and not l.strip().startswith("#")]
    if len(lineas) < LINEAS_MIN_BRIEF:
        return False, f"BRIEF.md tiene {len(lineas)} líneas (mínimo {LINEAS_MIN_BRIEF})"
    if not base:
        return True, "sin rama base para revisar el orden de commits"
    commits = (git("rev-list", "--reverse", f"{base}..HEAD") or "").split()
    primero_brief = primero_codigo = None
    for i, c in enumerate(commits):
        archivos = (git("show", "--name-only", "--format=", c) or "").splitlines()
        if primero_brief is None and "BRIEF.md" in archivos:
            primero_brief = i
        if primero_codigo is None and any(a.startswith(("agent/", "evals/", "Dockerfile")) for a in archivos):
            primero_codigo = i
    if primero_brief is None:
        return False, "BRIEF.md no está en ningún commit"
    if primero_codigo is not None and primero_codigo <= primero_brief:
        return False, "el brief se commiteó después (o junto con) el primer cambio de código"
    return True, "brief commiteado antes del código"


def auditoria(no_arregladas):
    path = ROOT / "AUDIT.md"
    if not path.exists():
        return []
    texto = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
    partes = re.split(r"^#{2,4}\s*(F\d{2})\b.*$", texto, flags=re.M)
    validas = []
    for i in range(1, len(partes) - 1, 2):
        fid, cuerpo = partes[i].upper(), partes[i + 1]
        if fid in no_arregladas and len(cuerpo.split()) >= PALABRAS_MIN_AUDITORIA and fid not in validas:
            validas.append(fid)
    return validas


def resolver_base(base):
    for cand in ([base] if base else ["origin/main", "main"]):
        if git("rev-parse", "--verify", "--quiet", cand):
            return cand
    return None


def calcular(base=None):
    base = resolver_base(base)
    tests = correr_tests()
    detalle, total = {}, 0
    brief_ok, brief_msg = brief(base)
    for fid, (tema, nombre, pts, bonus) in FALLAS.items():
        if fid == "F01":
            ok = brief_ok
        else:
            r = tests.get(fid, [])
            ok = bool(r) and all(r)
        ganados = (pts + bonus) if ok else 0
        total += ganados
        detalle[fid] = {"tema": tema, "nombre": nombre, "ok": ok, "puntos": ganados}
    no_arregladas = [f for f, d in detalle.items() if not d["ok"] and f != "F01"]
    auditadas = auditoria(no_arregladas)
    pts_audit = PUNTOS_AUDITORIA * len(auditadas)
    base_res = tests.get("BASE", [])
    rotos = base_res.count(False) if base_res else 4  # si ni siquiera corren, penalidad máxima
    penalidad = min(PENALIDAD_MAX, PENALIDAD_BASE * rotos)
    total += pts_audit - penalidad
    return {
        "total": total,
        "maximo": sum(p + b for _, _, p, b in FALLAS.values()),
        "arregladas": sum(1 for d in detalle.values() if d["ok"]),
        "fallas": detalle,
        "brief": brief_msg,
        "auditadas": auditadas,
        "puntos_auditoria": pts_audit,
        "tests_base_rotos": rotos,
        "penalidad": penalidad,
    }


def imprimir(r):
    print(f"\n  PUNTAJE: {r['total']} / {r['maximo']}   ({r['arregladas']}/{len(FALLAS)} fallas resueltas)\n")
    for fid, d in r["fallas"].items():
        marca = "✔" if d["ok"] else "·"
        print(f"  {marca} {fid}  {d['tema']:<19} {d['nombre']:<44} {d['puntos']:>3}")
    print(f"\n  Brief: {r['brief']}")
    print(f"  Auditoría: {len(r['auditadas'])} fallas bien documentadas (+{r['puntos_auditoria']}) {', '.join(r['auditadas'])}")
    print(f"  Tests base rotos: {r['tests_base_rotos']} (-{r['penalidad']})\n")


def markdown(r):
    print(f"## Puntaje: {r['total']} / {r['maximo']}\n")
    print("| | Falla | Tema | Puntos |\n|---|---|---|---|")
    for fid, d in r["fallas"].items():
        print(f"| {'✅' if d['ok'] else '⬜'} | {fid} {d['nombre']} | {d['tema']} | {d['puntos']} |")
    print(f"\nAuditoría: +{r['puntos_auditoria']} · Penalidad por tests base rotos: -{r['penalidad']} · Brief: {r['brief']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--base")
    a = ap.parse_args()
    res = calcular(a.base)
    if a.json:
        print(json.dumps(res, ensure_ascii=False))
    elif a.markdown:
        markdown(res)
    else:
        imprimir(res)
