# coding=utf-8
# Copyright (C) 2022  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from ..misc import only_digits
from .gtin import calcula_dv

GS1_SSCC_LENGTH = 18


def validar(sscc):
    """
    Código serial de contêiner de remessa

    ------- ------------------------------------------------------------------- ---
    SSCC       Dígitos do código                                                DV
    ------- ------------------------------------------------------------------- ---
    SSCC	N1	N2	N3	N4	N5	N6	N7	N8	N9	N10	N11	N12	N13	N14	N15	N16	N17	N18
            x3	x1	x3	x1	x3	x1	x3	x1	x3	x1	x3	x1	x3	x1	x3	x1	x3

    :param string sscc: SSCC para ser validado
    :return bool: True or False
    """

    # Limpando SSCC
    sscc = only_digits(sscc)

    # verificando o tamano do SSCC
    if len(sscc) != GS1_SSCC_LENGTH:
        return False

    # Pega apenas os 17 primeiros dígitos do SSCC para calcular o digito
    novo = calcula_dv(sscc[:17], GS1_SSCC_LENGTH)

    # Se o número gerado coincidir com o número original, é válido
    if novo == list(map(int, sscc)):
        return True

    return False
