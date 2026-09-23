# Guía del facilitador

## Cómo se mide (resumen)
Todo el puntaje es automático y sale del código, no de la opinión de un jurado:

1. **Tests por falla.** Hay 16 fallas (F01–F16), cada una con un archivo de tests. Una falla cuenta como arreglada solo si *todos* sus tests pasan. 10 puntos cada una; las 3 de seguridad valen 15.
2. **Brief primero (F01).** `score.py` revisa el historial de git: el commit que agrega `BRIEF.md` (con al menos 5 líneas reales) tiene que ser anterior al primer commit que toca `agent/`, `evals/` o `Dockerfile`. Esto mide la parte de *planificación* de ingeniería híbrida.
3. **Auditoría.** Por cada falla que NO arreglaron pero documentaron en `AUDIT.md` (sección `### FXX` con 30+ palabras) suman 3 puntos. Así quien programa más lento igual compite con criterio.
4. **Penalidad.** `tests/test_base.py` cubre lo que ya funcionaba. Cada test que rompan resta 5 (máximo −20).
5. **Anti-trampa.** El leaderboard califica cada PR con los tests, `score.py`, `conftest.py` y `pytest.ini` de `main`, no con los del equipo.

Máximo 170 puntos. Empate: gana quien hizo su último commit primero.

## Mapa de fallas vs. temario
| Falla | Tema | Qué se corrige |
|---|---|---|
| F01 | Ingeniería híbrida | Brief y plan antes de implementar |
| F02 | LLMOps · secretos | API key hardcodeada → variable de entorno |
| F03 | LLMOps · resiliencia | Timeout y reintentos acotados |
| F04 | LLMOps · costos | Modelo barato para tareas simples |
| F05 | Tools · idempotencia | `crear_ticket` no duplica con la misma llave |
| F06 | Tools · efectos secundarios | `borrar_usuario` exige confirmación |
| F07 | Tools · seguridad | Neutralizar prompt injection en documentos del RAG |
| F08 | Arquitecturas · ReAct | Límite de pasos y tools inexistentes |
| F09 | Arquitecturas · router | Enrutamiento sin depender de mayúsculas |
| F10 | RAG | Stopwords/normalización y fuente para citar |
| F11 | Memoria | Ventana acotada con lo más reciente |
| F12 | Evaluación · golden set | 8+ casos con bordes y adversariales |
| F13 | Evaluación · LLM-as-judge | Prompt con variables, escala 1–5, JSON y justificación |
| F14 | Observabilidad · tracing | Spans con duración y errores |
| F15 | Orquestación · MCP | Contrato (`input_schema`) para cada tool |
| F16 | Cloud | Dockerfile sin secretos, sin root y con healthcheck |
| — | Git/GitHub | Fork, rama, commits ordenados y PR (requisito para aparecer) |

## Preparación (el día anterior)
1. Crea el repo en GitHub con el contenido de `rescate-agente/` y márcalo como **template o público** para que puedan hacer fork.
2. En Settings → Actions, habilita que los workflows corran en PRs de forks (así cada equipo ve su puntaje en el PR).
3. Haz un ensayo: fork, rama, un arreglo, PR, y corre `python leaderboard.py` para ver que aparece.
4. Verifica que todos tengan cuenta de GitHub, Python 3.10+ y acceso a Claude.
5. **No subas la carpeta `solucion/`** al repo de los participantes.

## Durante el evento
| Minuto | Qué pasa |
|---|---|
| 0–2 | Kickoff: la historia, las reglas, la tabla de puntaje del README |
| 2–4 | Brief y commit del brief |
| 4–16 | Arreglos. Proyecta el leaderboard |
| 16–19 | Auditoría y PR |
| 19–20 | Leaderboard final |

En tu máquina, dentro del clon del repo oficial:
```bash
python leaderboard.py --watch 30
```
y abre `leaderboard.html` en el navegador del proyector (se refresca solo). Cada círculo amarillo es una falla resuelta, así se ve el avance en vivo.

Si los equipos no hacen fork sino que empujan ramas al repo oficial, pídeles igual que abran PR: el leaderboard lee `refs/pull/*`.

## Seguridad
El leaderboard ejecuta el código de los participantes. Córrelo en un Codespace o contenedor desechable, no en tu máquina con credenciales de trabajo.
