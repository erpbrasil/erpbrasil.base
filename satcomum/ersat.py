# -*- coding: utf-8 -*-
#
# satcomum/ersat.py
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

"""Este módulo fornece implementações para algumas características descritas na
ER SAT (*Especificação de Requisitos*) que não estão cobertas diretamente neste
projeto nem nos projetos relacionados com o SAT-CF-e.
"""

import re

from . import br
from . import constantes
from . import util


def meio_pagamento(codigo):
    """Obtém a descrição para o código do meio de pagamento.

    :param codigo: Código do meio de pagamento, conforme elemento WA03 ``cMP``.
    :return: Descrição para o código do meio de pagamento.
    :rtype: unicode

    .. sourcecode:: python

        >>> meio_pagamento('01')
        u'Dinheiro'

    """
    return [s for v,s in constantes.WA03_CMP_MP if v == codigo][0]


def dados_qrcode(cfe):
    """Compila os dados que compõem o QRCode do CF-e-SAT, conforme a
    documentação técnica oficial **Guia para Geração do QRCode pelo Aplicativo
    Comercial**, a partir de uma instância de ``ElementTree`` que represente a
    árvore do XML do CF-e-SAT.

    :param cfe: Instância de :py:mod:`xml.etree.ElementTree.ElementTree`.
    :return: String contendo a massa de dados para ser usada ao gerar o QRCode.
    :rtype: str

    Por exemplo, para gerar a imagem do QRCode [#qrcode]_:

    .. sourcecode:: python

        import xml.etree.ElementTree as ET
        import qrcode

        with open('CFe_1.xml', 'r') as fp:
            tree = ET.parse(fp)
            imagem = qrcode.make(dados_qrcode(tree))

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


class ChaveCFeSAT(object):
    """Representa a **chave de acesso** do CF-e-SAT conforme descrito na
    Especificação de Requisitos SAT, item 4.7. Os campos são definidos assim:

    .. sourcecode:: text

        0  2    6             20 22        31     37     43  --> índice
        |  |    |              |  |         |      |      |
        35 1508 08723218000186 59 900004019 000024 111425 7  --> campos
        |  |    |              |  |         |      |      |
        |  |    |              |  |         |      |      dígito verificador
        |  |    |              |  |         |      |
        |  |    |              |  |         |      código aleatório
        |  |    |              |  |         |
        |  |    |              |  |         número do cupom fiscal
        |  |    |              |  |
        |  |    |              |  número de série do equipamento SAT
        |  |    |              |
        |  |    |              modelo do documento fiscal
        |  |    |
        |  |    cnpj do emitente
        |  |
        |  ano/mês de emissão
        |
        código da UF


    .. sourcecode:: python

        >>> chave = ChaveCFeSAT('CFe35150808723218000186599000040190000241114257')
        >>> chave.codigo_uf
        35
        >>> chave.uf
        'SP'
        >>> chave.mes_emissao
        8
        >>> chave.ano_emissao
        2015
        >>> chave.anomes
        '1508'
        >>> chave.cnpj_emitente
        '08.723.218/0001-86'
        >>> chave.modelo_documento
        '59'
        >>> chave.numero_serie
        '900004019'
        >>> chave.numero_cupom_fiscal
        '000024'
        >>> chave.codigo_aleatorio
        '111425'
        >>> chave.digito_verificador
        '7'

        # chave com mês/ano no mês da Portaria CAT-147, introduzida em 11/2012
        >>> chave = ChaveCFeSAT('CFe35121108723218000186599000040190000241114259')
        >>> chave.mes_emissao
        11
        >>> chave.ano_emissao
        2012

        >>> chave = ChaveCFeSAT('CFe72150808723218000186599000040190000241114250')
        Traceback (most recent call last):
         ...
        ValueError: chave de acesso invalida (codigo UF: '72'): 'CFe72150808723218000186599000040190000241114250'

        >>> # mês/ano inválidos (Portaria CAT-147 introduzida em 11/2012)
        >>> chave = ChaveCFeSAT('CFe35121008723218000186599000040190000241114255')
        Traceback (most recent call last):
         ...
        ValueError: chave de acesso invalida (mes/ano emissao: 10/2012): 'CFe35121008723218000186599000040190000241114255'

        >>> # mês/ano inválidos (Portaria CAT-147 introduzida em 11/2012)
        >>> chave = ChaveCFeSAT('CFe35111208723218000186599000040190000241114250')
        Traceback (most recent call last):
         ...
        ValueError: chave de acesso invalida (mes/ano emissao: 12/2011): 'CFe35111208723218000186599000040190000241114250'

        >>> # mês/ano inválido (mês fora da faixa)
        >>> chave = ChaveCFeSAT('CFe35151308723218000186599000040190000241114251')
        Traceback (most recent call last):
         ...
        ValueError: chave de acesso invalida (mes/ano emissao: 13/2015): 'CFe35151308723218000186599000040190000241114251'

        >>> chave = ChaveCFeSAT('CFe35150808723218000187599000040190000241114259')
        Traceback (most recent call last):
         ...
        ValueError: chave de acesso invalida (CNPJ emitente: '08723218000187'): 'CFe35150808723218000187599000040190000241114259'


    """

    CHAVE_REGEX = re.compile(r'^CFe(?P<campos>\d{44})$')

    CUF = slice(0, 2)

    AAMM = slice(2, 6)

    CNPJ = slice(6, 20)

    MOD = slice(20, 22)

    NSERIESAT = slice(22, 31)

    NCF = slice(31, 37)

    CNF = slice(37, 43)

    CDV = slice(43, None)


    def __init__(self, chave):

        self._chave = None
        self._campos = None

        matcher = ChaveCFeSAT.CHAVE_REGEX.match(chave)
        if matcher:
            campos = matcher.group('campos')
        else:
            raise ValueError('chave de acesso invalida: {!r}'.format(chave))

        digito = util.modulo11(campos[:43])
        if not (digito == int(campos[-1])):
            raise ValueError('digito verificador invalido: '
                    'chave={!r}, digito calculado={!r}'.format(chave, digito))

        if not br.is_codigo_uf(int(campos[ChaveCFeSAT.CUF])):
            raise ValueError('chave de acesso invalida '
                    '(codigo UF: {!r}): {!r}'.format(
                            campos[ChaveCFeSAT.CUF], chave))

        ano = int(campos[ChaveCFeSAT.AAMM][:2]) + 2000
        mes = int(campos[ChaveCFeSAT.AAMM][2:])

        if mes not in xrange(1,13) or \
                (ano < 2012 or (ano == 2012 and mes < 11)):
            # considera válidas apenas as chaves que indicam mês/ano de emissão
            # a partir do início do projeto SAT-CF-e, em novembro/2012
            raise ValueError('chave de acesso invalida '
                    '(mes/ano emissao: {:d}/{:d}): {!r}'.format(
                            mes, ano, chave))

        if not br.is_cnpj(campos[ChaveCFeSAT.CNPJ]):
            raise ValueError('chave de acesso invalida '
                    '(CNPJ emitente: {!r}): {!r}'.format(
                            campos[ChaveCFeSAT.CNPJ], chave))

        self._chave = chave
        self._campos = campos


    def __repr__(self):
        return '{:s}({!r})'.format(self.__class__.__name__, str(self))


    def __unicode__(self):
        return self._chave


    def __str__(self):
        return unicode(self).encode('utf-8')


    @property
    def codigo_uf(self):
        return int(self._campos[ChaveCFeSAT.CUF])


    @property
    def uf(self):
        return br.uf_pelo_codigo(self.codigo_uf)


    @property
    def anomes(self):
        return self._campos[ChaveCFeSAT.AAMM]


    @property
    def ano_emissao(self):
        return int(self._campos[ChaveCFeSAT.AAMM][:2]) + 2000


    @property
    def mes_emissao(self):
        return int(self._campos[ChaveCFeSAT.AAMM][2:])


    @property
    def cnpj_emitente(self):
        return br.as_cnpj(self._campos[ChaveCFeSAT.CNPJ])


    @property
    def modelo_documento(self):
        return self._campos[ChaveCFeSAT.MOD]


    @property
    def numero_serie(self):
        return self._campos[ChaveCFeSAT.NSERIESAT]


    @property
    def numero_cupom_fiscal(self):
        return self._campos[ChaveCFeSAT.NCF]


    @property
    def codigo_aleatorio(self):
        return self._campos[ChaveCFeSAT.CNF]


    @property
    def digito_verificador(self):
        return self._campos[ChaveCFeSAT.CDV]


    def partes(self, num_partes=11):
        """Particiona a chave do CF-e-SAT em uma lista de *n* segmentos.

        :param int num_partes: O número de segmentos (partes) em que os digitos
            da chave do CF-e-SAT serão particionados. **Esse número deverá
            resultar em uma divisão inteira por 44 (o comprimento da chave)**.
            Se não for informado, assume ``11`` partes, comumente utilizado
            para apresentar a chave do CF-e-SAT no extrato.

        :return: Lista de strings contendo a chave do CF-e-SAT particionada.
        :rtype: list

        .. sourcecode:: python

            >>> chave = ChaveCFeSAT('CFe35150461099008000141599000017900000053222424')
            >>> chave.partes()
            ['3515', '0461', '0990', '0800', '0141', '5990', '0001', '7900', '0000', '5322', '2424']
            >>> chave.partes(2)
            ['3515046109900800014159', '9000017900000053222424']
            >>> chave.partes(3)
            Traceback (most recent call last):
             ...
            AssertionError: O numero de partes nao produz um resultado inteiro (partes por 44 digitos): num_partes=3

        """
        assert 44 % num_partes == 0, 'O numero de partes nao produz um '\
                'resultado inteiro (partes por 44 digitos): '\
                'num_partes=%s' % num_partes

        salto = 44 / num_partes
        return [self._campos[n:(n + salto)] for n in range(0, 44, salto)]
