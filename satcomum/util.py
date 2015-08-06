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

from . import constantes


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


def dados_qrcode(cfe):
    """Compila os dados que compõem o QRCode do CF-e-SAT a partir do elemento
    :py:mod:`xml.etree.ElementTree` que representa a árvore do XML do CF-e-SAT,
    conforme a documentação técnica oficial **Guia para Geração do QRCode pelo
    Aplicativo Comercial**.

    Por exemplo, para gerar a imagem do QRCode [#qrcode]_:

    .. sourcecode:: python

        import xml.etree.ElementTree as ET
        import qrcode

        with open('CFe_1.xml', 'r') as fp:
            tree = ET.parse(fp)
            imagem = qrcode.make(dados_qrcode(tree))

    :return: String contendo a massa de dados para ser usada ao gerar o QRCode.

    .. [#qrcode] https://pypi.python.org/pypi/qrcode

    """
    infCFe = cfe.getroot().find('./infCFe')
    cnpjcpf_consumidor = infCFe.findtext('dest/CNPJ') or \
            infCFe.findtext('dest/CPF') or ''
    return '|'.join([
            infCFe.attrib['Id'][3:], # remove prefixo "CFe"
            '{}{}'.format(
                    infCFe.findtext('ide/dEmi'),
                    infCFe.findtext('ide/hEmi')),
            infCFe.findtext('total/vCFe'),
            cnpjcpf_consumidor,
            infCFe.findtext('ide/assinaturaQRCODE'),])


def meio_pagamento(codigo):
    """Retorna a descrição para o código do meio de pagamento, referente ao
    elemento ``cMP`` WA03.

    .. sourcecode:: python

        >>> meio_pagamento('01')
        u'Dinheiro'

    """
    return [s for v,s in constantes.WA03_CMP_MP if v == codigo][0]


def partes_chave_cfe(chave, partes=11):
    """Retorna a chave de consulta do CF-e-SAT em uma lista de segmentos onde a
    chave de acesso em si (com 44 dígitos) está particionada em *N* partes.

    .. sourcecode:: python

        >>> chave = '35150461099008000141599000017900000053222424'
        >>> partes_chave_cfe(chave)
        ['3515', '0461', '0990', '0800', '0141', '5990', '0001', '7900', '0000', '5322', '2424']
        >>> partes_chave_cfe(chave, partes=2)
        ['3515046109900800014159', '9000017900000053222424']
        >>> partes_chave_cfe(chave, partes=3)
        Traceback (most recent call last):
         ...
        AssertionError: O numero de partes nao produz um resultado inteiro (partes por 44 digitos): partes=3

    """
    assert 44 % partes == 0, 'O numero de partes nao produz um resultado '\
            'inteiro (partes por 44 digitos): partes=%s' % partes
    salto = 44 / partes
    _chave = chave.replace('CFe', '') # remove o prefixo 'CFe' se houver
    return [_chave[n:(n + salto)] for n in range(0, 44, salto)]
