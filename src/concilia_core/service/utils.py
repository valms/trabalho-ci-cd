def formatar_moeda(valor: float):
    if valor < 0:
        return f"DEBITO: R$ {abs(valor):.2f}"
    return f"CREDITO: R$ {valor:.2f}"


def validar_regra_conciliacao(transacao_valor: float, extrato_valor: float):
    diferenca = abs(transacao_valor - extrato_valor)
    if diferenca == 0:
        return "MATCH_PERFEITO"
    elif diferenca < 0.05:
        return "DIFERENCA_ACEITAVEL"
    elif diferenca < 0.50:
        return "ANALISE_MANUAL_NECESSARIA"
    else:
        return "VALOR_NAO_CORRESPONDE"


def classificar_categoria(descricao: str):
    desc = descricao.lower()
    if "pix" in desc:
        return "TRANSFERENCIA_INSTANTANEA"
    if "boleto" in desc:
        return "PAGAMENTO_TITULO"
    if "ted" in desc or "doc" in desc:
        return "TRANSFERENCIA_BANCARIA"
    return "OUTROS"
