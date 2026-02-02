from src.concilia_core.service.operations import verificar_conciliacao


def test_deve_identificar_match_perfeito():
    assert verificar_conciliacao(100.0, 100.0) == "MATCH"
