# coding=utf-8
# Copyright (C) 2022  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import re
import random

from .gtin import calcula_dv
from ..misc import only_digits

GS1_GSIN_LENGTH = 17


def validar(gsin):
    """
    Número de identificação de remessa global

    ------- --------------------------------------------------------------- ---
    GSIN       Dígitos do código                                            DV
    ------- --------------------------------------------------------------- ---
    GSIN    N1	N2	N3	N4	N5	N6	N7	N8	N9	N10	N11	N12	N13	N14	N15	N16	N17
            x1	x3	x1	x3	x1	x3	x1	x3	x1	x3	x1	x3	x1	x3	x1	x3

    :param string gsin: GSIN para ser validado
    :return bool: True or False
    """

    # Limpando GSIN
    gsin = only_digits(gsin)

    # verificando o tamano do GSIN
    if len(gsin) != GS1_GSIN_LENGTH:
        return False

    # Pega apenas os 16 primeiros dígitos do GSIN para calcular o digito
    novo = calcula_dv(gsin[:16], GS1_GSIN_LENGTH)

    # Se o número gerado coincidir com o número original, é válido
    if novo == list(map(int, gsin)):
        return True

    return False
