# coding=utf-8
# Copyright (C) 2014  Renato Lima - Akretion
# Copyright (C) 2015  Luis Felipe Mileo - KMEE
# Copyright (C) 2015  Base4 Sistemas Ltda ME
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import re
import string


def only_digits(string_value):
    """Retorna somente os números de uma string"""
    if string_value.isdigit():
        tmp_value = string_value
    else:
        tmp_value = re.sub("[^0-9]", "", string_value)
    return tmp_value


def punctuation_rm(string_value):
    """Remove pontuações de uma string: !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""
    tmp_value = re.sub("[%s]" % re.escape(string.punctuation), "", string_value or "")
    return tmp_value


def calc_price_ratio(price_gross, amount_calc, amount_total):
    if amount_total:
        return price_gross * amount_calc / amount_total
    else:
        return 0.0


def format_zipcode(zipcode, country_code="BR"):
    zipcode_formatted = zipcode or ""
    if zipcode and country_code.upper() == "BR":
        val = re.sub("[^0-9]", "", zipcode)
        if len(val) == 8:
            zipcode_formatted = "%s-%s" % (val[0:5], val[5:8])
    return zipcode_formatted


def modulo11(base):
    """Calcula o dígito verificador (DV) para o argumento usando "Módulo 11".
    :param str base: String contendo os dígitos sobre os quais o DV será
        calculado, assumindo que o DV não está incluído no argumento.
    :return: O dígito verificador calculado.

    Source: https://github.com/base4sistemas/satcomum/blob/f45da5b100a63511b9c455cbd6895b630e121866/satcomum/util.py

    :rtype: int
    """
    pesos = "23456789" * ((len(base) // 8) + 1)
    acumulado = sum([int(a) * int(b) for a, b in zip(base[::-1], pesos)])
    digito = 11 - (acumulado % 11)
    return 0 if digito >= 10 else digito
