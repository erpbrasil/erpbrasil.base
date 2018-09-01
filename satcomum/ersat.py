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

from six.moves import range

from . import br
from . import constantes
from . import util


def meio_pagamento(codigo):
    """Obtém a descrição para o código do meio de pagamento.

    :param codigo: Código do meio de pagamento, conforme elemento WA03 ``cMP``.
    :return: Descrição para o código do meio de pagamento.
    :rtype: unicode

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

        if mes not in range(1,13) or \
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

        """
        assert 44 % num_partes == 0, 'O numero de partes nao produz um '\
                'resultado inteiro (partes por 44 digitos): '\
                'num_partes=%s' % num_partes

        salto = 44 // num_partes
        return [self._campos[n:(n + salto)] for n in range(0, 44, salto)]
