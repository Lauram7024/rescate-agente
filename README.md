# Rescate del agente en producción

Ayer salió a producción el agente de soporte interno: responde preguntas con RAG, crea tickets y consulta el directorio de usuarios. Hoy está causando incidentes. Eres el equipo de guardia y tienes **20 minutos** antes de la reunión con el CTO.

## Reglas
- Individual o equipos de hasta 3 personas.
- Puedes (y deberías) usar Claude / Claude Code. Tú decides, la IA ejecuta, tú revisas.
- Hay 16 fallas plantadas y no te va a alcanzar el tiempo para todas. Prioriza.
- Entregas con un **Pull Request** a `main`. Lo que no esté en el PR no cuenta.

## Arranque (2 minutos)
```bash
# 1. Haz fork del repo en GitHub y clónalo
git clone https://github.com/<tu-usuario>/rescate-agente.git
cd rescate-agente
git checkout -b equipo-<nombre>
pip install -r requirements.txt

# 2. Mira tu puntaje en cualquier momento
python score.py
```

## Paso a paso
1. **Llena `TEAM.md`** con el nombre del equipo y los integrantes.
2. **Escribe `BRIEF.md` y haz commit SOLO de ese archivo** antes de tocar código. Si el brief llega después del primer cambio de código, no suma.
3. **Arregla.** Cada falla tiene su test en `tests/test_fXX_*.py`: léelo, es la especificación. Corre `python score.py` seguido.
4. **Audita** en `AUDIT.md` las fallas que encontraste y no alcanzaste a arreglar.
5. **Abre el Pull Request** antes de que suene el minuto 19.

## Puntaje
| Qué | Puntos |
|---|---|
| Cada falla arreglada (todos sus tests en verde) | 10 |
| Bonus por las de seguridad: F02 secretos, F06 confirmación, F07 prompt injection | +5 c/u |
| Brief commiteado antes del código (F01) | 5 |
| Cada falla no arreglada pero bien auditada (sección `### FXX` con 30+ palabras) | 3 |
| Cada test de `tests/test_base.py` que rompas | −5 (máx. −20) |

Máximo: 170. Empate: gana quien hizo su último commit primero.

> Los tests oficiales se restauran al calificar. Editar `tests/` o `score.py` no cambia tu puntaje final.
