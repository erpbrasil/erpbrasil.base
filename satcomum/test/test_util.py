# -*- coding: utf-8 -*-
#
# satcomum/test/test_util.py
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

from decimal import Decimal

import pytest

from satcomum import util


def test_digitos():
    assert util.digitos('teste') == ''
    assert util.digitos('2015-08-20') == '20150820'


def test_texto_decimal():
    valor = Decimal('10.0000')
    assert util.texto_decimal(valor) == '10'
    assert util.texto_decimal(valor, remover_zeros=False) == '10.0000'
    assert util.texto_decimal(Decimal('10.00100')) == '10.001'
    assert util.texto_decimal(Decimal('-1.00')) == '-1'
    assert util.texto_decimal(Decimal('-0.010')) == '-0.01'


def test_modulo_11():
    assert util.modulo11('0') == 0 # digito resultante: 11
    assert util.modulo11('6') == 0 # digito resultante: 10
    assert util.modulo11('1') == 9 # digito resultante: 9

    # chaves de CF-e-SAT emitidos em ambiente de testes
    # CFe35150808723218000186599000040190000241114257
    # CFe35150808723218000186599000040190000253347537
    assert util.modulo11('3515080872321800018659900004019000024111425') == 7
    assert util.modulo11('3515080872321800018659900004019000025334753') == 7


def test_validar_casas_decimais():
    assert util.validar_casas_decimais(Decimal('0.1')) is None
    assert util.validar_casas_decimais(Decimal('0.12')) is None
    assert util.validar_casas_decimais(Decimal('0'), minimo=0) is None
    assert util.validar_casas_decimais(Decimal('0.1230'), maximo=4) is None

    with pytest.raises(ValueError):
        # o número deveria possuir no mínimo 1 e no máximo 2 casas decimais
        util.validar_casas_decimais(Decimal('1.001'))

    with pytest.raises(ValueError):
        # o número deveria possuir no mínimo 1 e no máximo 2 casas decimais
        util.validar_casas_decimais(Decimal('1'))
