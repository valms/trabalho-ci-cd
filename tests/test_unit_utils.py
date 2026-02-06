from src.concilia_core.service.utils import (
    formatar_moeda,
    validar_regra_conciliacao,
    classificar_categoria
)


# def test_formatacao_moeda_brasil():
#     assert formatar_moeda(150.50) == "CREDITO: R$ 150.50"
#     assert formatar_moeda(-50.0) == "DEBITO: R$ 50.00"
#
#
# def test_validacao_de_diferencas_conciliacao():
#     assert validar_regra_conciliacao(10.0, 10.0) == "MATCH_PERFEITO"
#     assert validar_regra_conciliacao(10.0, 10.04) == "DIFERENCA_ACEITAVEL"
#     assert validar_regra_conciliacao(10.0, 10.40) == "ANALISE_MANUAL_NECESSARIA"
#     assert validar_regra_conciliacao(10.0, 20.0) == "VALOR_NAO_CORRESPONDE"
#
#
# def test_categorizacao_por_keyword():
#     assert classificar_categoria("Recebi via PIX") == "TRANSFERENCIA_INSTANTANEA"
#     assert classificar_categoria("Boleto internet") == "PAGAMENTO_TITULO"
#     assert classificar_categoria("TED para conta") == "TRANSFERENCIA_BANCARIA"
#     assert classificar_categoria("Almoço") == "OUTROS"
