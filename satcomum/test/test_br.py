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

import string

import pytest

from satcomum import br


def test_uf():
    assert br.uf('SP') is None # UF OK
    with pytest.raises(br.UnidadeFederativaError):
        br.uf('sp')


def test_is_uf():
    assert not br.is_uf('')
    assert not br.is_uf('sp')
    assert br.is_uf('SP')


def test_is_codigo_uf():
    assert br.is_codigo_uf(35) # 35 código de SP
    assert not br.is_codigo_uf(0)


def test_uf_pelo_codigo():
    assert br.uf_pelo_codigo(35) == 'SP'
    with pytest.raises(ValueError):
        br.uf_pelo_codigo(0)


def test_codigo_ibge_uf():
    assert br.codigo_ibge_uf('SP') == 35
    for uf in ('sp', '',): # lista de UF inválidas
        with pytest.raises(ValueError):
            br.codigo_ibge_uf(uf)


def test_cnpj():
    invalidos = (
            '123', # número CNPJ deve possuir 14 dígitos
            '08427847000179', # primeiro dígito DV errado
            '08427847000168', # segundo dígito DV errado
        )
    for numero in invalidos:
        with pytest.raises(br.NumeroCNPJError):
            br.cnpj(numero)

    # todos os dígitos iguais validam o DV mas formam um CNPJ inválido
    for digito in string.digits:
        with pytest.raises(br.NumeroCNPJError):
            br.cnpj(digito * 14)

    # CNPJ OK
    assert br.cnpj('08427847000169') is None


def test_is_cnpj():
    assert not br.is_cnpj('')
    assert br.is_cnpj('08.427.847/0001-69') # com mas máscara, não estrito, OK
    assert not br.is_cnpj('08.427.847/0001-69', estrito=True) # com máscara, estrito, deve falhar


def test_as_cnpj():
    assert br.as_cnpj('08427847000169') == '08.427.847/0001-69'
    assert br.as_cnpj('08427847000168') == '08427847000168' # segundo dígito DV inválido
    assert br.as_cnpj('08.427.847/0001-69') == '08.427.847/0001-69' # número CNPJ original válido, já mascarado, é OK
    assert br.as_cnpj('') == '' # número inválido devolve o que recebeu intocado
    assert br.as_cnpj('000') == '000'


def test_cpf():
    invalidos = (
            '123', # número CPF deve possuir 11 dígitos
            '11122233386', # primeiro dígito DV errado
            '11122233395', # segundo dígito DV errado
        )
    for numero in invalidos:
        with pytest.raises(br.NumeroCPFError):
            br.cpf(numero)

    # todos os dígitos iguais validam o DV mas formam um CPF inválido
    for digito in string.digits:
        with pytest.raises(br.NumeroCPFError):
            br.cpf(digito * 11)

    # CPF OK
    assert br.cpf('11122233396') is None


def test_is_cpf():
    assert not br.is_cpf('')
    assert br.is_cpf('111.222.333-96') # com máscara, não estrito, OK
    assert not br.is_cpf('111.222.333-96', estrito=True) # com máscara, estrito, deve falhar


def test_as_cpf():
    assert br.as_cpf('11122233396') == '111.222.333-96'
    assert br.as_cpf('111.222.333-96') == '111.222.333-96'
    assert br.as_cpf('') == '' # número inválido devolve o que recebeu intocado
    assert br.as_cpf('000') == '000'


def test_cnpjcpf():
    assert br.cnpjcpf('08427847000169') is None
    assert br.cnpjcpf('11122233396') is None
    with pytest.raises(br.NumeroCNPJCPFError):
        br.cnpjcpf('08427847000168') # não é um CNPJ ou CPF válido


def test_is_cnpjcpf():
    assert br.is_cnpjcpf('111.222.333-96')
    assert br.is_cnpjcpf('08.427.847/0001-69')
    assert not br.is_cnpjcpf('')
    assert not br.is_cnpjcpf('111.222.333-96', estrito=True)
    assert not br.is_cnpjcpf('08.427.847/0001-69', estrito=True)


def test_as_cnpjcpf():
    assert br.as_cnpjcpf('11122233396') == '111.222.333-96'
    assert br.as_cnpjcpf('111.222.333-96') == '111.222.333-96'
    assert br.as_cnpjcpf('08427847000169') == '08.427.847/0001-69'
    assert br.as_cnpjcpf('08.427.847/0001-69') == '08.427.847/0001-69'
    assert br.as_cnpjcpf('') == ''
    assert br.as_cnpjcpf('000') == '000'


def test_cep():
    assert br.cep('15807250') is None # OK, este existe mesmo, é válido
    assert br.cep('12345678') is None # OK, considera válido

    with pytest.raises(br.NumeroCEPError):
        br.cep('123456') # CEP "123456" não possui 8 dígitos

    for digito in string.digits:
        with pytest.raises(br.NumeroCEPError):
            br.cep(digito * 8) # 8 digitos mas todos iguais, considera inválido


def test_is_cep():
    assert not br.is_cep('')
    assert br.is_cep('15807-250')
    assert not br.is_cep('15807-250', estrito=True)


def test_as_cep():
    assert br.as_cep('15807250') == '15807-250'
    assert br.as_cep('15807-250') == '15807-250'
    assert br.as_cep('') == ''
    assert br.as_cep('123456') == '123456'
