#!/usr/bin/env python3
"""Leaderboard del facilitador. Califica cada Pull Request abierto contra los tests oficiales de main.

    python leaderboard.py              # califica una vez
    python leaderboard.py --watch 30   # recalifica cada 30 s (para proyectar)

Genera leaderboard.html (se refresca solo) y lo muestra en la terminal.
Los tests, score.py, conftest.py y pytest.ini se toman SIEMPRE de main: si un equipo los editó, no cuenta.
"""
import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / ".lb"
OFICIALES = ["tests", "score.py", "conftest.py", "pytest.ini"]
CACHE: dict[str, dict] = {}


def git(*args, cwd=ROOT, check=True):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout.strip()


def listar_prs(remote):
    salida = git("ls-remote", remote, "refs/pull/*/head")
    prs = []
    for linea in salida.splitlines():
        sha, ref = linea.split()
        prs.append((int(ref.split("/")[2]), sha))
    return sorted(prs)


def calificar(remote, numero, sha, base_sha):
    if sha in CACHE:
        return CACHE[sha]
    git("fetch", "-q", remote, f"+refs/pull/{numero}/head:refs/lb/pr-{numero}")
    wt = WORK / f"pr-{numero}"
    if wt.exists():
        git("worktree", "remove", "--force", str(wt), check=False)
        shutil.rmtree(wt, ignore_errors=True)
    git("worktree", "add", "-q", "--detach", str(wt), sha)
    for ruta in OFICIALES:
        destino = wt / ruta
        if destino.is_dir():
            shutil.rmtree(destino)
        elif destino.exists():
            destino.unlink()
        git("checkout", base_sha, "--", ruta, cwd=wt)
    equipo = f"PR #{numero}"
    team = wt / "TEAM.md"
    if team.exists():
        m = re.search(r"Equipo:\s*(.+)", team.read_text(encoding="utf-8"))
        if m and m.group(1).strip():
            equipo = m.group(1).strip()
    try:
        r = subprocess.run([sys.executable, "score.py", "--json", "--base", base_sha],
                           cwd=wt, capture_output=True, text=True, timeout=240)
        res = json.loads(r.stdout)
    except Exception as e:
        res = {"total": 0, "arregladas": 0, "error": str(e), "fallas": {}}
    res["equipo"] = equipo
    res["pr"] = numero
    res["ultimo_commit"] = int(git("log", "-1", "--format=%ct", sha))
    CACHE[sha] = res
    return res


def ranking(remote):
    git("fetch", "-q", remote, "main")
    base_sha = git("rev-parse", "FETCH_HEAD")
    WORK.mkdir(exist_ok=True)
    filas = [calificar(remote, n, s, base_sha) for n, s in listar_prs(remote)]
    # Desempate: más puntos, luego quien terminó primero (último commit más temprano)
    filas.sort(key=lambda r: (-r["total"], r["ultimo_commit"]))
    return filas


def terminal(filas):
    print("\033[2J\033[H" if sys.stdout.isatty() else "", end="")
    print(f"LEADERBOARD · {datetime.now():%H:%M:%S}\n")
    print(f"{'#':>2}  {'Equipo':<28} {'Puntos':>6}  {'Fallas':>6}  Auditadas")
    for i, r in enumerate(filas, 1):
        print(f"{i:>2}  {r['equipo'][:28]:<28} {r['total']:>6}  {r.get('arregladas', 0):>4}/16  {len(r.get('auditadas', []))}")
    if not filas:
        print("   (todavía no hay Pull Requests)")


def pagina(filas, refresco):
    temas = ["F%02d" % i for i in range(1, 17)]
    filas_html = []
    for i, r in enumerate(filas, 1):
        celdas = "".join(
            f"<td class='f {'ok' if r.get('fallas', {}).get(t, {}).get('ok') else ''}' title='{t}'></td>" for t in temas
        )
        filas_html.append(
            f"<tr class='{'top' if i <= 3 else ''}'><td class='pos'>{i}</td><td class='eq'>{html.escape(r['equipo'])}</td>"
            f"<td class='pts'>{r['total']}</td>{celdas}</tr>"
        )
    cab = "".join(f"<th>{t[1:]}</th>" for t in temas)
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="{refresco}"><title>Rescate del agente · Leaderboard</title>
<style>
:root{{--ink:#171719;--yellow:#f6f072;--lav:#a9a0ec;--sky:#d4e0ed}}
body{{margin:0;background:var(--ink);color:#fff;font-family:"Stack Sans Text",system-ui,-apple-system,Segoe UI,Roboto,sans-serif;padding:48px}}
h1{{font-size:56px;letter-spacing:-.03em;margin:0 0 4px}} h1 span{{color:var(--yellow)}}
p{{color:var(--sky);margin:0 0 32px;font-size:18px}}
table{{border-collapse:separate;border-spacing:0 8px;width:100%}}
th{{color:var(--lav);font-weight:500;font-size:13px;text-align:center}}
td{{padding:14px 10px;background:#232327}} td:first-child{{border-radius:999px 0 0 999px;padding-left:24px}}
td:last-child{{border-radius:0 999px 999px 0}}
.pos{{font-size:28px;font-weight:800;width:48px}} .eq{{font-size:24px;font-weight:600}}
.pts{{font-size:32px;font-weight:800;color:var(--yellow);text-align:right;padding-right:24px}}
.f{{width:22px}} .f::after{{content:"";display:block;width:14px;height:14px;border-radius:50%;border:2px solid #444;margin:auto}}
.f.ok::after{{background:var(--yellow);border-color:var(--yellow)}}
tr.top .pos{{color:var(--yellow)}}
</style></head><body>
<h1>Rescate del agente<span>.</span></h1>
<p>Actualizado {datetime.now():%H:%M:%S} · {len(filas)} equipos · máximo 170 puntos</p>
<table><tr><th></th><th style="text-align:left">Equipo</th><th style="text-align:right;padding-right:24px">Puntos</th>{cab}</tr>
{''.join(filas_html) or '<tr><td colspan="19">Esperando Pull Requests…</td></tr>'}
</table></body></html>"""


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--remote", default="origin")
    ap.add_argument("--watch", type=int, default=0, help="segundos entre actualizaciones")
    a = ap.parse_args()
    while True:
        filas = ranking(a.remote)
        (ROOT / "leaderboard.html").write_text(pagina(filas, max(a.watch, 15)), encoding="utf-8")
        (ROOT / "leaderboard.json").write_text(json.dumps(filas, ensure_ascii=False, indent=1), encoding="utf-8")
        terminal(filas)
        if not a.watch:
            break
        time.sleep(a.watch)
