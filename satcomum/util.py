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
