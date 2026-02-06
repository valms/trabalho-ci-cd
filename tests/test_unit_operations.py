from src.concilia_core.service.operations import ConciliaService, verificar_conciliacao


def test_deve_identificar_match_e_divergencia():
    assert verificar_conciliacao(100.0, 100.0) == "MATCH"
    assert verificar_conciliacao(100.0, 50.0) == "DIVERGENTE"


def test_fluxo_registro_transacao():
    service = ConciliaService()

    tx_id = service.save_transaction("Mensalidade Faculdade", 1200.00)
    assert isinstance(tx_id, int)

    status = service.get_transaction_status(tx_id)
    assert status == "PENDING"


def test_status_transacao_inexistente():
    service = ConciliaService()
    assert service.get_transaction_status(9999) is None
