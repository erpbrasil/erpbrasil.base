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
            assinaturaqrcode = infCFe.findtext('ide/assinaturaQRCODE'))


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
