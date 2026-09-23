from agent.rag import retrieve

CASOS = [
    ("¿Cuántos días de vacaciones tengo al año?", "politica_vacaciones"),
    ("No me conecta la VPN desde la casa", "soporte_vpn"),
    ("¿Cómo pido el reembolso de un gasto de viaje?", "reembolsos"),
    ("¿A qué hora atiende la mesa de ayuda el sábado?", "mesa_de_ayuda"),
]


def test_el_documento_correcto_sale_primero():
    for query, esperado in CASOS:
        res = retrieve(query)
        assert res[0]["id"] == esperado, f"{query!r} -> {res[0]['id']!r}"


def test_resultados_traen_fuente_para_citar():
    for r in retrieve("vacaciones"):
        assert r.get("source"), "cada resultado debe traer 'source' para poder citar"
