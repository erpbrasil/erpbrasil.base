# coding=utf-8
# Copyright (C) 2013  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import re


def validar(cnpj_cpf=None):
    """Função básica para validação de um CNPJ ou CPF depedendo da
    quantidade de digitos (sem acentuação), caso a string tenha 14 digitos
    será considerado como um CNPJ, caso tenha 11 será considerado como um CPF.
    :Parameters:
      - 'cnpj_cpf': CNPJ ou CPF para ser validado.
    :Return: True or False
    """
    if not cnpj_cpf:
        return
    cnpj_cpf = re.sub('[^0-9]', '', cnpj_cpf)

    if len(cnpj_cpf) == 14:
        return validar_cnpj(cnpj_cpf)

    if len(cnpj_cpf) == 11:
        return validar_cpf(cnpj_cpf)


def validar_cnpj(cnpj):
    """ Rotina para validação do CNPJ - Cadastro Nacional
    de Pessoa Juridica.
    :param string cnpj: CNPJ para ser validado
    :return bool: True or False
    """
    # Limpando o cnpj
    if not cnpj.isdigit():
        cnpj = re.sub('[^0-9]', '', cnpj)

    # verificando o tamano do  cnpj
    if len(cnpj) != 14:
        return False

    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os digitos
    cnpj = list(map(int, cnpj))
    novo = cnpj[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    # Se o número gerado coincidir com o número original, é válido
    if novo == cnpj:
        return True

    return False


def validar_cpf(cpf):
    """Rotina para validação do CPF - Cadastro Nacional
    de Pessoa Física.
    :Return: True or False
    :Parameters:
      - 'cpf': CPF to be validate.
    """
    # Limpando o cpf
    if not cpf.isdigit():
        cpf = re.sub('[^0-9]', '', cpf)

    if len(cpf) != 11 or cpf == cpf[0] * len(cpf):
        return False

    # Pega apenas os 9 primeiros dígitos do CPF e gera os 2 dígitos que faltam
    cpf = list(map(int, cpf))
    novo = cpf[:9]

    while len(novo) < 11:
        r = sum([(len(novo) + 1 - i) * v for i, v in enumerate(novo)]) % 11

        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)

    # Se o número gerado coincidir com o número original, é válido
    if novo == cpf:
        return True
    return False


def formata(cnpj_cpf=None):
    if not cnpj_cpf:
        return
    cnpj_cpf = re.sub('[^0-9]', '', cnpj_cpf)
    if len(cnpj_cpf) == 14:
        cnpj_cpf = formata_cnpj(cnpj_cpf)

    if len(cnpj_cpf) == 11:
        cnpj_cpf = formata_cpf(cnpj_cpf)

    return cnpj_cpf


def formata_cnpj(cnpj=None):
    cnpj = re.sub('[^0-9]', '', cnpj)
    if len(cnpj) == 14:
        cnpj = "%s.%s.%s/%s-%s" % (cnpj[0:2],
                                   cnpj[2:5],
                                   cnpj[5:8],
                                   cnpj[8:12],
                                   cnpj[12:14])

    return cnpj


def formata_cpf(cpf=None):
    cpf = re.sub('[^0-9]', '', cpf)
    if len(cpf) == 11:
        cpf = "%s.%s.%s-%s" % (cpf[0:3],
                               cpf[3:6],
                               cpf[6:9],
                               cpf[9:11])

    return cpf
