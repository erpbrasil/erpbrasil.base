# -*- coding: utf-8 -*-
#
# satcomum/tests/test_ersat.py
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

import collections
import io
import xml.etree.ElementTree as ET

import pytest

from satcomum import ersat


_QRCODE_CHAVECONSULTA = 0
_QRCODE_TIMESTAMP = 1
_QRCODE_VALORTOTAL = 2
_QRCODE_CPFCNPJVALUE = 3
_QRCODE_ASSINATURAQRCODE = 4


AtributosQRCode = collections.namedtuple('AtributosQRCode',
        'chaveconsulta timestamp valortotal cpfcnpjvalue assinaturaqrcode')


def _atributos_qrcode(tree):
    infCFe = tree.getroot().find('./infCFe')
    cpfcnpjvalue = infCFe.findtext('dest/CPF') or \
            infCFe.findtext('dest/CNPJ') or ''
    return AtributosQRCode(
            chaveconsulta=infCFe.attrib['Id'][3:],
            timestamp=infCFe.findtext('ide/dEmi') + infCFe.findtext('ide/hEmi'),
            valortotal=infCFe.findtext('total/vCFe'),
            cpfcnpjvalue=cpfcnpjvalue,
            assinaturaqrcode=infCFe.findtext('ide/assinaturaQRCODE'))


def _assert_dados_qrcode(tree):
    dados = ersat.dados_qrcode(tree)

    campos = dados.split('|')
    assert len(campos) == 5

    atributos = _atributos_qrcode(tree)
    assert campos[_QRCODE_CHAVECONSULTA] == atributos.chaveconsulta
    assert campos[_QRCODE_TIMESTAMP] == atributos.timestamp
    assert campos[_QRCODE_VALORTOTAL] == atributos.valortotal
    assert campos[_QRCODE_CPFCNPJVALUE] == atributos.cpfcnpjvalue
    assert campos[_QRCODE_ASSINATURAQRCODE] == atributos.assinaturaqrcode


def test_qrcode_venda(xml_venda):
    tree = ET.parse(io.StringIO(xml_venda))
    _assert_dados_qrcode(tree)


def test_qrcode_cancelamento(xml_cancelamento):
    tree = ET.parse(io.StringIO(xml_cancelamento))
    _assert_dados_qrcode(tree)


def test_meio_pagamento():
    assert ersat.meio_pagamento('01') == 'Dinheiro'


def test_chave_cfesat():
    chave = ersat.ChaveCFeSAT('CFe35150808723218000186599000040190000241114257')
    assert chave.codigo_uf == 35
    assert chave.uf == 'SP'
    assert chave.mes_emissao == 8
    assert chave.ano_emissao == 2015
    assert chave.anomes == '1508'
    assert chave.cnpj_emitente == '08.723.218/0001-86'
    assert chave.modelo_documento == '59'
    assert chave.numero_serie == '900004019'
    assert chave.numero_cupom_fiscal == '000024'
    assert chave.codigo_aleatorio == '111425'
    assert chave.digito_verificador == '7'


def test_chave_cfesat_2012_11():
    # chave com mês/ano no mês da Portaria CAT-147, introduzida em 11/2012
    chave = ersat.ChaveCFeSAT('CFe35121108723218000186599000040190000241114259')
    assert chave.mes_emissao == 11
    assert chave.ano_emissao == 2012


def test_chave_cfesat_invalidas():
    invalidas = (
            'CFe72150808723218000186599000040190000241114250', # código UF 72 invalido
            'CFe35121008723218000186599000040190000241114255', # mês/ano inválidos (Portaria CAT-147 introduzida em 11/2012)
            'CFe35111208723218000186599000040190000241114250', # mês/ano inválidos (Portaria CAT-147 introduzida em 11/2012)
            'CFe35151308723218000186599000040190000241114251', # mês/ano inválido (mês fora da faixa)
            'CFe35150808723218000187599000040190000241114259', # número do CNPJ emitente inválido
        )

    for chave in invalidas:
        with pytest.raises(ValueError):
            ersat.ChaveCFeSAT(chave)


def test_chave_cfesat_partes():
    chave = ersat.ChaveCFeSAT('CFe35150461099008000141599000017900000053222424')
    assert chave.partes(2) == ['3515046109900800014159', '9000017900000053222424']
    assert chave.partes() == [
            # padrão, dividindo em 11 partes
            '3515',
            '0461',
            '0990',
            '0800',
            '0141',
            '5990',
            '0001',
            '7900',
            '0000',
            '5322',
            '2424',]

    with pytest.raises(AssertionError):
        chave.partes(3) # o número de partes deve ser divisível por 44
