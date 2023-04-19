# Copyright (C) 2023  Tiago Amaral - KMEE
# License MIT - See https://opensource.org/license/mit/


def validar(bacen):
    """Essa função valida o "Código de País" conforme tabela do BACEN (Banco Central do Brasil)."""
    if not bacen.isdigit():
        return False
    bacen = bacen.zfill(4)
    if len(bacen) > 4:
        return False
    pesos = [4, 3, 2]
    digitos = list(map(lambda digito: int(digito), bacen))

    soma = 0
    for i in range(0, 3):
        soma += pesos[i] * digitos[i]

    modulo = soma % 11
    if modulo == 0 or modulo == 1:
        digito_verificador = 0
    else:
        digito_verificador = 11 - modulo

    if digito_verificador != digitos[3]:
        return False
    return True
