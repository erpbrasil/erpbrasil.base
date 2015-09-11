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
    """Resulta em uma string contendo apenas os dígitos da string original.

    .. sourcecode:: python

        >>> digitos('teste')
        ''
        >>> digitos('2015-08-20')
        '20150820'

    """
    return ''.join([d for d in valor if d.isdigit()])


def texto_decimal(valor, remover_zeros=True):
    """Converte um valor :py:class:`decimal.Decimal` para texto, com a opção de
    remover os zeros à direita não significativos. A conversão para texto irá
    considerar o :py:module:`locale` para converter o texto pronto para
    apresentação.

    :param decimal.Decimal valor: Valor a converter para texto.
    :param bool remover_zeros: *Opcional* Indica se os zeros à direita não
        significativos devem ser removidos do texto, o que irá incluir o
        separador decimal se for o caso.

    .. sourcecode:: python

        >>> from decimal import Decimal
        >>> valor = Decimal('10.0000')
        >>> texto_decimal(valor)
        '10'
        >>> texto_decimal(valor, remover_zeros=False)
        '10.0000'
        >>> texto_decimal(Decimal('10.00100'))
        '10.001'
        >>> texto_decimal(Decimal('-1.00'))
        '-1'
        >>> texto_decimal(Decimal('-0.010'))
        '-0.01'

    """
    texto = '{:n}'.format(valor)
    if remover_zeros:
        dp = locale.localeconv().get('decimal_point')
        texto = texto.rstrip('0').rstrip(dp) if dp in texto else texto
    return texto


def forcar_unicode(arg):
    """Força uma conversão do argumento para unicode, se necessário.

    .. sourcecode:: python

        >>> forcar_unicode('teste')
        u'teste'
        >>> forcar_unicode(u'teste')
        u'teste'
        >>> forcar_unicode(1)
        Traceback (most recent call last):
         ...
        TypeError: ...

    """
    if isinstance(arg, unicode):
        return arg
    elif isinstance(arg, str):
        return arg.decode('utf-8')

    raise TypeError(
            'Expected unicode or str; got {!r} ({!r})'.format(arg, type(arg)))


def modulo11(base):
    """Calcula o dígito verificador (DV) para o argumento usando "Módulo 11".

    :param str base: String contendo os dígitos sobre os quais o DV será
        calculado, assumindo que o DV não está incluído no argumento.

    :return: O dígito verificador calculado.
    :rtype: int

    .. sourcecode:: python

        >>> modulo11('0')  # digito resultante: 11
        0
        >>> modulo11('6')  # digito resultante: 10
        0
        >>> modulo11('1')  # digito resultante: 9
        9

        # chaves de CF-e-SAT emitidos em ambiente de testes
        # CFe35150808723218000186599000040190000241114257
        # CFe35150808723218000186599000040190000253347537
        >>> modulo11('3515080872321800018659900004019000024111425')
        7
        >>> modulo11('3515080872321800018659900004019000025334753')
        7

    """
    pesos = '23456789' * ((len(base) / 8) + 1)
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

    .. sourcecode:: python

        >>> from decimal import Decimal
        >>> validar_casas_decimais(Decimal('0.1'))
        >>> validar_casas_decimais(Decimal('0.12'))
        >>> validar_casas_decimais(Decimal('0'), minimo=0)
        >>> validar_casas_decimais(Decimal('0.1230'), maximo=4)

        >>> validar_casas_decimais(Decimal('1.001'))
        Traceback (most recent call last):
         ...
        ValueError: Numero de casas decimais fora dos limites esperados (valor=Decimal('1.001'), minimo=1, maximo=2): DecimalTuple(sign=0, digits=(1, 0, 0, 1), exponent=-3)

        >>> validar_casas_decimais(Decimal('1'))
        Traceback (most recent call last):
         ...
        ValueError: Numero de casas decimais fora dos limites esperados (valor=Decimal('1'), minimo=1, maximo=2): DecimalTuple(sign=0, digits=(1,), exponent=0)


    :raises ValueError: Se o valor possuir um número de casas decimais fora dos
        limites mínimo e máximo informados.

    """
    atributos = valor.as_tuple()
    if not (minimo <= abs(atributos.exponent) <= maximo):
        raise ValueError('Numero de casas decimais fora dos limites esperados '
                '(valor={!r}, minimo={!r}, maximo={!r}): {!r}'.format(
                        valor, minimo, maximo, atributos))
