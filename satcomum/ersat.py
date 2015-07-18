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


class ChaveCFeSAT(object):
    """Chave de acesso do CF-e-SAT conforme descrito na ER SAT, item 4.7.

    .. todo:: calcular e validar o dígito verificador

    .. sourcecode:: python

        >>> chave = ChaveCFeSAT('CFe35150708723218000186599000040190000050939770')
        >>> chave.codigo_uf
        35
        >>> chave.uf
        'SP'
        >>> chave.mes_emissao
        7
        >>> chave.ano_emissao
        2015
        >>> chave.cnpj_emitente
        '08.723.218/0001-86'
        >>> chave.modelo_documento
        '59'
        >>> chave.numero_serie
        '900004019'
        >>> chave.numero_cupom_fiscal
        '000005'
        >>> chave.codigo_aleatorio
        '093977'
        >>> chave.digito_verificador
        '0'

        # chave com mês/ano no mês da Portaria CAT-147, introduzida em 11/2012
        >>> chave = ChaveCFeSAT('CFe35121108723218000186599000040190000050939770')
        >>> chave.mes_emissao
        11
        >>> chave.ano_emissao
        2012

        >>> chave = ChaveCFeSAT('CFe72150708723218000186599000040190000050939770')
        Traceback (most recent call last):
         ...
        ValueError: chave de acesso invalida (codigo UF: 72): 'CFe72150708723218000186599000040190000050939770'

        >>> # mês/ano inválidos (Portaria CAT-147 introduzida em 11/2012)
        >>> chave = ChaveCFeSAT('CFe35121008723218000186599000040190000050939770')
        Traceback (most recent call last):
         ...
        ValueError: chave de acesso invalida (mes/ano emissao: 10/2012): 'CFe35121008723218000186599000040190000050939770'

        >>> # mês/ano inválidos (Portaria CAT-147 introduzida em 11/2012)
        >>> chave = ChaveCFeSAT('CFe35111208723218000186599000040190000050939770')
        Traceback (most recent call last):
         ...
        ValueError: chave de acesso invalida (mes/ano emissao: 12/2011): 'CFe35111208723218000186599000040190000050939770'

        >>> # mês/ano inválido (mês fora da faixa)
        >>> chave = ChaveCFeSAT('CFe35151308723218000186599000040190000050939770')
        Traceback (most recent call last):
         ...
        ValueError: chave de acesso invalida (mes/ano emissao: 13/2015): 'CFe35151308723218000186599000040190000050939770'

        >>> chave = ChaveCFeSAT('CFe35150708723218000187599000040190000050939770')
        Traceback (most recent call last):
         ...
        ValueError: chave de acesso invalida (CNPJ emitente: '08723218000187'): 'CFe35150708723218000187599000040190000050939770'


    """

    def __init__(self, chave):
        match = re.match(r'^CFe(?P<campos>\d{44})$', chave)
        if not match:
            raise ValueError('chave de acesso invalida: {!r}'.format(chave))

        campos = match.group('campos')
        #
        #  0  2    6             20 22        31     37     43  -- indice
        #  |  |    |              |  |         |      |      |
        #  35 1507 08723218000186 59 900004019 000005 093977 0  -- campos
        #  |  |    |              |  |         |      |      |
        #  |  |    |              |  |         |      |      digito verificador
        #  |  |    |              |  |         |      |
        #  |  |    |              |  |         |      codigo aleatorio
        #  |  |    |              |  |         |
        #  |  |    |              |  |         numero do cupom fiscal
        #  |  |    |              |  |
        #  |  |    |              |  numero de serie do equipamento SAT
        #  |  |    |              |
        #  |  |    |              modelo do documento fiscal
        #  |  |    |
        #  |  |    cnpj do emitente
        #  |  |
        #  |  ano/mes de emissao
        #  |
        #  codigo da UF
        #
        codigo_uf = int(campos[0:2], 10)
        ano = int(campos[2:4], 10) + 2000
        mes = int(campos[4:6], 10)
        cnpj_emitente = campos[6:20]
        modelo_documento = campos[20:22]
        numero_serie = campos[22:31]
        numero_cupom_fiscal = campos[31:37]
        codigo_aleatorio = campos[37:43]
        digito_verificador = campos[43:]

        if not br.is_codigo_uf(codigo_uf):
            raise ValueError('chave de acesso invalida '
                    '(codigo UF: {!r}): {!r}'.format(codigo_uf, chave))

        if mes not in xrange(1,13) or \
                (ano < 2012 or (ano == 2012 and mes < 11)):
            raise ValueError('chave de acesso invalida '
                    '(mes/ano emissao: {:d}/{:d}): {!r}'.format(
                            mes, ano, chave))

        if not br.is_cnpj(cnpj_emitente):
            raise ValueError('chave de acesso invalida '
                    '(CNPJ emitente: {!r}): {!r}'.format(
                            cnpj_emitente, chave))

        self._chave = chave
        self._codigo_uf = codigo_uf
        self._uf = br.uf_pelo_codigo(codigo_uf)
        self._ano_emissao = ano
        self._mes_emissao = mes
        self._cnpj_emitente = cnpj_emitente
        self._modelo_documento = modelo_documento
        self._numero_serie = numero_serie
        self._numero_cupom_fiscal = numero_cupom_fiscal
        self._codigo_aleatorio = codigo_aleatorio
        self._digito_verificador = digito_verificador


    def __repr__(self):
        return '{:s}({!r})'.format(self.__class__.__name__, str(self))


    def __unicode__(self):
        return self._chave


    def __str__(self):
        return unicode(self).encode('utf-8')


    @property
    def codigo_uf(self):
        return self._codigo_uf


    @property
    def uf(self):
        return self._uf


    @property
    def ano_emissao(self):
        return self._ano_emissao


    @property
    def mes_emissao(self):
        return self._mes_emissao


    @property
    def cnpj_emitente(self):
        return br.as_cnpj(self._cnpj_emitente)


    @property
    def modelo_documento(self):
        return self._modelo_documento


    @property
    def numero_serie(self):
        return self._numero_serie


    @property
    def numero_cupom_fiscal(self):
        return self._numero_cupom_fiscal


    @property
    def codigo_aleatorio(self):
        return self._codigo_aleatorio


    @property
    def digito_verificador(self):
        return self._digito_verificador

