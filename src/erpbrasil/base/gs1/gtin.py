# coding=utf-8
# Copyright (C) 2022  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import random

from ..misc import only_digits

GS1_GTIN_LENGTH = 14


def calcula_dv(gs1_code, code_length):
    if type(gs1_code) is not list:
        gs1_code = list(map(int, gs1_code))
    prod = [3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3, 1, 3]

    # get the product with some gs1_code length
    gs1_prod = prod[len(prod) - len(gs1_code) :]

    while len(gs1_code) < code_length:
        r = sum([x * y for (x, y) in zip(gs1_code, gs1_prod)]) % 10
        if r > 0:
            f = 10 - r
        else:
            f = 0
        gs1_code.append(f)

    return gs1_code


def validar(gtin):
    """
    Rotina para calcular o dígito verificador dos códigos:

    - GTIN-8
    - GTIN-12/UPC-A
    - GTIN-13/EAN-13
    - GTIN-13/ITF-14

    0   0   6   1   4   1   4   1   9   9   9   9   9   6
    -----   ---------------------   -----------------   -
    |               |                       |           |
    |               |                       |           Dígito verificador
    |               |                       |
    |               |                       Referência do item
    |               |
    |               GS1 Préfixo da empresa
    |
    Dígito N1

    Como calcular o dígito verificador:

    ---------- ---------------------------------------------------- ---
    GTIN       Dígitos do código                                    DV
    ---------- ---------------------------------------------------- ---
    GTIN-8	 	 	 	 	 	 	 	N1	N2	N3	N4	N5	N6	N7	N8
    GTIN-12	 	 	 	N1	N2	N3	N4	N5	N6	N7	N8	N9	N10	N11	N12
    GTIN-13	 	 	N1	N2	N3	N4	N5	N6	N7	N8	N9	N10	N11	N12	N13
    GTIN-14	 	N1	N2	N3	N4	N5	N6	N7	N8	N9	N10	N11	N12	N13	N14
    -------------------------------------------------------------------
                x3	x1	x3	x1	x3	x1	x3	x1	x3	x1	x3	x1	x3

    Para calcular o último digito (DV), caso o GTIN tenha menos do que 14 digitos
    será preenchido com zeros a esquerda.

    Exemplo de calculo:

    Para calcular o dígito verificador do GTIN-13 629104150021-

                N1	N2	N3	N4	N5	N6	N7	N8	N9	N10	N11	N12	N13
    GTIN-13 	6	2	9	1	0	4	1	5	0	0	2	1	-
    Multiplica	x	x	x	x	x	x	x	x	x	x	x	x	-
    por     	1	3	1	3	1	3	1	3	1	3	1	3	-
                =	=	=	=	=	=	=	=	=	=	=	=	-
    Soma        6	6	9	3	0	12	1	15	0	0	2	3	-

    Soma todos os resultados:
    6 + 6 + 9 + 3 + 0 + 12 + 1 + 15 + 0 + 0 + 2 + 3 = 57

    Subtraia a soma do múltiplo de dez mais próximo igual ou superior:
    60 - 57 = 3 Dígito verificador

    GTIN-13: 6291041500213

    :param string gtin: GTIN para ser validado
    :return bool: True or False
    """

    # Limpando gtin
    gtin = only_digits(gtin)

    # verificando o tamano do gtin
    if len(gtin) < 8 or len(gtin) > 14:
        return False

    # Iguala qualquer GTIN adicionando zeros a equerda
    gtin = gtin.zfill(14)

    # Pega apenas os 13 primeiros dígitos do GTIN e gera os digitos
    novo = calcula_dv(gtin[:13], GS1_GTIN_LENGTH)

    # Se o número gerado coincidir com o número original, é válido
    print(novo, " == ", list(map(int, gtin)))
    if novo == list(map(int, gtin)):
        return True

    return False


def gerar_gs1_code(gs1_code_length, prefill=1):
    gs1_codes = []
    for _ in range(prefill):
        code = [random.randint(0, 9) for x in range(gs1_code_length - 1)]
        gs1_code = calcula_dv(code, gs1_code_length)
        gs1_codes.append("".join(map(str, gs1_code)))

    return gs1_codes if len(gs1_codes) > 1 else gs1_codes[0]
