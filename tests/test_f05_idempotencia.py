import uuid

from agent import tools


def test_reintento_con_misma_llave_no_duplica():
    tools.reset()
    key = str(uuid.uuid4())
    a = tools.crear_ticket("VPN", "no conecta", idempotency_key=key)
    b = tools.crear_ticket("VPN", "no conecta", idempotency_key=key)
    assert a["id"] == b["id"]
    assert len(tools.TICKETS) == 1


def test_llaves_distintas_crean_tickets_distintos():
    tools.reset()
    a = tools.crear_ticket("A", "x", idempotency_key=str(uuid.uuid4()))
    b = tools.crear_ticket("B", "y", idempotency_key=str(uuid.uuid4()))
    assert a["id"] != b["id"] and len(tools.TICKETS) == 2
