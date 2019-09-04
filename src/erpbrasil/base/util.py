# -*- coding: utf-8 -*-
#
# satcomum/util.py
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

import locale


def digitos(valor):
    """Resulta em uma string contendo apenas os dígitos da string original."""
    return ''.join([d for d in valor if d.isdigit()])


def texto_decimal(valor, remover_zeros=True):
    """Converte um valor :py:class:`decimal.Decimal` para texto, com a opção de
    remover os zeros à direita não significativos. A conversão para texto irá
    considerar o :mod:`locale` para converter o texto pronto para
    apresentação.

    :param decimal.Decimal valor: Valor a converter para texto.
    :param bool remover_zeros: *Opcional* Indica se os zeros à direita não
        significativos devem ser removidos do texto, o que irá incluir o
        separador decimal se for o caso.

    """
    texto = '{:n}'.format(valor)
    if remover_zeros:
        dp = locale.localeconv().get('decimal_point')
        texto = texto.rstrip('0').rstrip(dp) if dp in texto else texto
    return texto


def modulo11(base):
    """Calcula o dígito verificador (DV) para o argumento usando "Módulo 11".

    :param str base: String contendo os dígitos sobre os quais o DV será
        calculado, assumindo que o DV não está incluído no argumento.

    :return: O dígito verificador calculado.
    :rtype: int

    """
    pesos = '23456789' * ((len(base) // 8) + 1)
    acumulado = sum([int(a) * int(b) for a, b in zip(base[::-1], pesos)])
    digito = 11 - (acumulado % 11)
    return 0 if digito >= 10 else digito


def validar_casas_decimais(valor, minimo=1, maximo=2):
    """Valida o número de casas decimais. Se o número de casas decimais não
    estiver dentro do mínimo e máximo, será lançada uma exceção do tipo
    :py:exc:`ValueError`.

    :param valor: Um objeto :py:class:`~decimal.Decimal`.

    :param minimo: Valor inteiro maior ou igual a zero indicando o número
        mínimo de casas decimais. Se não informado, ``1`` é o mínimo.

    :param maximo: Valor inteiro maior ou igual a zero indicando o número
        máximo de casas decimais. Se não informado, ``2`` é o máximo.

    :raises ValueError: Se o valor possuir um número de casas decimais fora dos
        limites mínimo e máximo informados.

    """
    atributos = valor.as_tuple()
    if not (minimo <= abs(atributos.exponent) <= maximo):
        raise ValueError((
                'Numero de casas decimais fora dos limites esperados '
                '(valor={!r}, minimo={!r}, maximo={!r}): {!r}'
            ).format(valor, minimo, maximo, atributos))
