# -*- coding: utf-8 -*-
#
# satcomum/br.py
#
# Copyright 2015 Base4 Sistemas Ltda ME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from .util import digitos


class NumeroCNPJError(ValueError):
    pass


class NumeroCPFError(ValueError):
    pass


class NumeroCNPJCPFError(NumeroCNPJError, NumeroCPFError):
    pass


class NumeroCEPError(ValueError):
    pass


class UnidadeFederativaError(ValueError):
    pass


REGIAO_NORTE = u'Norte'
REGIAO_NORDESTE = u'Nordeste'
REGIAO_CENTRO_OESTE = u'Centro Oeste'
REGIAO_SUDESTE = u'Sudeste'
REGIAO_SUL = u'Sul'

_UF_SIGLA = 0
_UF_CODIGO_IBGE = 1
_UF_NOME = 2
_UF_REGIAO = 3

UNIDADES_FEDERACAO = (
        # sigla, código IBGE, nome, região
        ('AC', 12, u'Acre', REGIAO_NORTE),
        ('AL', 27, u'Alagoas', REGIAO_NORDESTE),
        ('AM', 13, u'Amazonas', REGIAO_NORTE),
        ('AP', 16, u'Amapá', REGIAO_NORTE),
        ('BA', 29, u'Bahia', REGIAO_NORDESTE),
        ('CE', 23, u'Ceará', REGIAO_NORDESTE),
        ('DF', 53, u'Distrito Federal', REGIAO_CENTRO_OESTE),
        ('ES', 32, u'Espírito Santo', REGIAO_SUDESTE),
        ('GO', 52, u'Goiás', REGIAO_CENTRO_OESTE),
        ('MA', 21, u'Maranhão', REGIAO_NORDESTE),
        ('MG', 31, u'Minas Gerais', REGIAO_SUDESTE),
        ('MS', 50, u'Mato Grosso do Sul', REGIAO_CENTRO_OESTE),
        ('MT', 51, u'Mato Grosso', REGIAO_CENTRO_OESTE),
        ('PA', 15, u'Pará', REGIAO_NORTE),
        ('PB', 25, u'Paraíba', REGIAO_NORDESTE),
        ('PE', 26, u'Pernambuco', REGIAO_NORDESTE),
        ('PI', 22, u'Piauí', REGIAO_NORDESTE),
        ('PR', 41, u'Paraná', REGIAO_SUL),
        ('RJ', 33, u'Rio de Janeiro', REGIAO_SUDESTE),
        ('RN', 24, u'Rio Grande de Norte', REGIAO_NORDESTE),
        ('RO', 11, u'Rondônia', REGIAO_NORTE),
        ('RR', 14, u'Roraima', REGIAO_NORTE),
        ('RS', 43, u'Rio Grande do Sul', REGIAO_SUL),
        ('SC', 42, u'Santa Catarina', REGIAO_SUL),
        ('SE', 28, u'Sergipe', REGIAO_NORDESTE),
        ('SP', 35, u'São Paulo', REGIAO_SUDESTE),
        ('TO', 17, u'Tocantins', REGIAO_NORTE),)


def uf(sigla):
    """
    Valida a sigla da Unidade Federativa. Se não for uma sigla de UF válida,
    será lançada a exceção :exc:`UnidadeFederativaError`.
    """
    if sigla not in [s for s, i, n, r in UNIDADES_FEDERACAO]:
        raise UnidadeFederativaError((
                'Estado (sigla) UF inexistente: {!r}'
            ).format(sigla))


def is_uf(sigla):
    """Uma versão conveniente para usar em testes condicionais. Apenas retorna
    verdadeiro ou falso, conforme o argumento é validado.
    """
    try:
        uf(sigla)
        return True
    except UnidadeFederativaError:
        pass
    return False


def is_codigo_uf(codigo_ibge):
    """Indica se o código da UF é um código válido."""
    return codigo_ibge in [i for s, i, n, r in UNIDADES_FEDERACAO]


def uf_pelo_codigo(codigo_ibge):
    """Retorna a UF para o código do IBGE informado."""
    idx = [i for s, i, n, r in UNIDADES_FEDERACAO].index(codigo_ibge)
    return UNIDADES_FEDERACAO[idx][_UF_SIGLA]


def codigo_ibge_uf(sigla):
    """Retorna o código do IBGE para a UF informada."""
    idx = [s for s, i, n, r in UNIDADES_FEDERACAO].index(sigla)
    return UNIDADES_FEDERACAO[idx][_UF_CODIGO_IBGE]


def cnpj(numero):
    """Valida um número de CNPJ. O número deverá ser informado como uma string
    contendo 14 dígitos numéricos. Se o número informado for inválido será
    lançada a exceção :exc:`NumeroCNPJError`. Esta implementação da validação
    foi delicadamente copiada de `python-sped <http://git.io/vfuGW>`."""
    _digitos = [int(c) for c in numero if c.isdigit()]

    if len(_digitos) != 14 or len(numero) != 14:
        raise NumeroCNPJError('Nao possui 14 digitos: {!r}'.format(numero))

    if numero == numero[0] * 14:
        raise NumeroCNPJError('Todos os digitos iguais: {!r}'.format(numero))

    multiplicadores = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    soma1 = sum([_digitos[i] * multiplicadores[i+1] for i in range(12)])
    soma2 = sum([_digitos[i] * multiplicadores[i] for i in range(13)])
    digito1 = 11 - (soma1 % 11)
    digito2 = 11 - (soma2 % 11)

    if digito1 >= 10:
        digito1 = 0

    if digito2 >= 10:
        digito2 = 0

    if _digitos[12] != digito1 or _digitos[13] != digito2:
        raise NumeroCNPJError((
                'Digitos verificadores invalidos: {!r}'
            ).format(numero))


def is_cnpj(numero, estrito=False):
    """Uma versão conveniente para usar em testes condicionais. Apenas retorna
    verdadeiro ou falso, conforme o argumento é validado.

    :param bool estrito: Padrão ``False``, indica se apenas os dígitos do
        número deverão ser considerados. Se verdadeiro, potenciais caracteres
        que formam a máscara serão removidos antes da validação ser realizada.

    """
    try:
        cnpj(digitos(numero) if not estrito else numero)
        return True
    except NumeroCNPJError:
        pass
    return False


def as_cnpj(numero):
    """Formata um número de CNPJ. Se o número não for um CNPJ válido apenas
    retorna o argumento sem qualquer modificação.
    """
    _num = digitos(numero)
    if is_cnpj(_num):
        return '{}.{}.{}/{}-{}'.format(
                _num[:2], _num[2:5], _num[5:8], _num[8:12], _num[12:])
    return numero


def cpf(numero):
    """Valida um número de CPF. O número deverá ser informado como uma string
    contendo 11 dígitos numéricos. Se o número informado for inválido será
    lançada a exceção :exc:`NumeroCPFError`. Esta implementação da validação
    foi delicadamente copiada de `python-sped <http://git.io/vfuGW>`.
    """
    _digitos = [int(c) for c in numero if c.isdigit()]

    if len(_digitos) != 11 or len(numero) != 11:
        raise NumeroCPFError('Nao possui 11 digitos: {!r}'.format(numero))

    if numero == numero[0] * 11:
        raise NumeroCPFError('Todos os digitos iguais: {!r}'.format(numero))

    multiplicadores = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]

    soma1 = sum([_digitos[i] * multiplicadores[i+1] for i in range(9)])
    soma2 = sum([_digitos[i] * multiplicadores[i] for i in range(10)])
    digito1 = 11 - (soma1 % 11)
    digito2 = 11 - (soma2 % 11)

    if digito1 >= 10:
        digito1 = 0

    if digito2 >= 10:
        digito2 = 0

    if _digitos[9] != digito1 or _digitos[10] != digito2:
        raise NumeroCPFError((
                'Digitos verificadores invalidos: {!r}'
            ).format(numero))


def is_cpf(numero, estrito=False):
    """Uma versão conveniente para usar em testes condicionais. Apenas retorna
    verdadeiro ou falso, conforme o argumento é validado.

    :param bool estrito: Padrão ``False``, indica se apenas os dígitos do
        número deverão ser considerados. Se verdadeiro, potenciais caracteres
        que formam a máscara serão removidos antes da validação ser realizada.

    """
    try:
        cpf(digitos(numero) if not estrito else numero)
        return True
    except NumeroCPFError:
        pass
    return False


def as_cpf(numero):
    """Formata um número de CPF. Se o número não for um CPF válido apenas
    retorna o argumento sem qualquer modificação.
    """
    _num = digitos(numero)
    if is_cpf(_num):
        return '{}.{}.{}-{}'.format(_num[:3], _num[3:6], _num[6:9], _num[9:])
    return numero


def cnpjcpf(numero):
    """Valida um número de CNPJ ou CPF. Veja :func:`cnpj` e/ou :func:`cpf`."""
    try:
        cnpj(numero)
    except NumeroCNPJError:
        try:
            cpf(numero)
        except NumeroCPFError:
            raise NumeroCNPJCPFError((
                    'Numero nao valida como CNPJ nem como CPF: {!r}'
                ).format(numero))


def is_cnpjcpf(numero, estrito=False):
    """Uma versão conveniente para usar em testes condicionais. Apenas retorna
    verdadeiro ou falso, conforme o argumento é validado.

    :param bool estrito: Padrão ``False``, indica se apenas os dígitos do
        número deverão ser considerados. Se verdadeiro, potenciais caracteres
        que formam a máscara serão removidos antes da validação ser realizada.

    """
    _numero = digitos(numero) if not estrito else numero
    try:
        cnpj(_numero)
        return True
    except NumeroCNPJError:
        try:
            cpf(_numero)
            return True
        except NumeroCPFError:
            pass
    return False


def as_cnpjcpf(numero):
    """Formata um número de CNPJ ou CPF. Se o número não for um CNPJ ou CPF
    válidos apenas retorna o argumento sem qualquer modificação.
    """
    if is_cnpj(numero):
        return as_cnpj(numero)
    elif is_cpf(numero):
        return as_cpf(numero)
    return numero


def cep(numero):
    """Valida um número de CEP. O número deverá ser informado como uma string
    contendo 8 dígitos numéricos. Se o número informado for inválido será
    lançada a exceção :exc:`NumeroCEPError`.

    .. warning::

        Qualquer string que contenha 8 dígitos será considerada como um CEP
        válido, desde que os dígitos não sejam todos iguais.

    """
    _digitos = digitos(numero)

    if len(_digitos) != 8 or len(numero) != 8:
        raise NumeroCEPError('CEP nao possui 8 digitos: {!r}'.format(numero))

    elif _digitos[0] * 8 == _digitos:
        raise NumeroCEPError('CEP invalido: {!r}'.format(numero))


def is_cep(numero, estrito=False):
    """Uma versão conveniente para usar em testes condicionais. Apenas retorna
    verdadeiro ou falso, conforme o argumento é validado.

    :param bool estrito: Padrão ``False``, indica se apenas os dígitos do
        número deverão ser considerados. Se verdadeiro, potenciais caracteres
        que formam a máscara serão removidos antes da validação ser realizada.

    """
    try:
        cep(digitos(numero) if not estrito else numero)
        return True
    except NumeroCEPError:
        pass
    return False


def as_cep(numero):
    """Formata um número de CEP. Se o argumento não for um CEP válido apenas
    retorna o argumento sem qualquer modificação.
    """
    _numero = digitos(numero)
    if is_cep(_numero):
        return '{}-{}'.format(_numero[:5], _numero[5:])
    return numero
