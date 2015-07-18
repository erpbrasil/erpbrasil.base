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

import logging
import xml.etree.ElementTree as ET

from decimal import Decimal

from . import constantes

logger = logging.getLogger('satcomum')


def digitos(valor):
    """Resulta em uma string contendo apenas os dígitos da string original.

    .. sourcecode:: python

        >>> digitos('teste')
        ''
        >>> digitos('2015-08-20')
        '20150820'

    """
    return ''.join([d for d in valor if d.isdigit()])


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
    raise TypeError('Expected unicode or str; got %s', type(arg))


def dados_qrcode(xml):
    """Compila os dados do QRCode conforme a documentação técnica oficial
    **Guia para Geração do QRCode pelo Aplicativo Comercial**.

    :param xml: Uma string contendo o XML do CF-e de venda ou cancelamento ou
        um objeto :class:`XMLFacade`, para o qual serão compilados os dados.
    """
    if isinstance(xml, basestring):
        xml = XMLFacadeFromString(xml)

    dados = [
            xml.attr('infCFe', 'Id')[3:], # remove prefixo "CFe"
            '{}{}'.format(
                    xml.text('infCFe/ide/dEmi'),
                    xml.text('infCFe/ide/hEmi')),
            xml.text('infCFe/total/vCFe'),
            xml.text('infCFe/dest/CPF',
                    alternative_xpath='infCFe/dest/CNPJ', default=''),
            xml.text('infCFe/ide/assinaturaQRCODE'),]
    return '|'.join(dados)


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


class XMLPathError(Exception):
    def __init__(self, xpath, filename, message, alternative_xpath=None):
        super(XMLPathError, self).__init__(
                '%s (xpath "%s", alternative xpath "%s", file "%s")' % (
                        message,
                        xpath,
                        alternative_xpath or '',
                        filename,))


class XMLFacade(object):
    """Um façade para lidar com arquivos XML através de algo parecido
    com *XPath*, mas com expectativas mais modestas.
    """

    def __init__(self, filename, namespace=None):
        self.namespace = namespace
        self.filename = filename
        self.fhandler = None
        self.tree = None
        self.root = None
        self.element = None
        self._begin_processing()


    def _begin_processing(self):
        try:
            self.fhandler = open(self.filename, 'rb')
            self.tree = ET.parse(self.fhandler)
            self.root = self.tree.getroot()
            self.element = XMLElementFacade(
                    self.root, self.filename, self.namespace)
        except:
            logger.exception('error opening XML "%s"', self.filename)
            raise


    def text(self, xpath, default=None, alternative_xpath=None):
        return self.element.text(xpath,
                default=default,
                alternative_xpath=alternative_xpath)


    def attr(self, xpath, attribute_name, default=None):
        return self.element.attr(xpath, attribute_name, default=default)


    def root_attr(self, attribute_name, default=None):
        if attribute_name not in self.root.attrib:
            if default is not None:
                return default
            raise AttributeNotFound(attribute_name)
        return self.root.attrib[attribute_name]


    def iterate(self, xpath):
        for el in self.element.iterate(xpath):
            yield el


    def done(self):
        try:
            self.fhandler.close()
        except:
            logger.exception('closing file handler for "%s"', self.filename)


    def decimal(self, xpath, default=None, alternative_xpath=None):
        str_value = self.text(xpath,
                default=default, alternative_xpath=alternative_xpath)
        return Decimal(str_value)


class XMLElementFacade(object):
    """Um façade para elementos ``xml.etree.ElementeTree`` oriúndos
    de :class:`XMLFacade`.
    """

    def __init__(self, root_node, filename, namespace):
        self.root = root_node
        self.filename = filename
        self.namespace = namespace


    def text(self, xpath, default=None, alternative_xpath=None):
        element = self._el(xpath)
        if element is None and alternative_xpath is not None:
            element = self._el(alternative_xpath)
        if element is None:
            if default is not None:
                return default
            raise XMLPathError(xpath, self.filename, 'xpath cannot be found',
                    alternative_xpath=alternative_xpath)
        return element.text


    def attr(self, xpath, attribute_name, default=None):
        try:
            element = self._el(xpath)

            if element is None:
                if default is not None:
                    return default
                raise XMLPathError(xpath, self.filename, 'xpath is None')

            if attribute_name not in element.attrib:
                if default is not None:
                    return default
                raise XMLPathError(xpath, self.filename,
                        'xpath does not have attribute "%s"' % attribute_name)

            return element.attrib[attribute_name]
        except:
            logger.exception('error getting attribute "%s" from "%s" '
                    '(file "%s")', attribute_name, xpath, self.filename)
            raise


    def root_attr(self, attribute_name, default=None):
        if attribute_name not in self.root.attrib:
            if default is not None:
                return default
            raise AttributeNotFound(attribute_name)
        return self.root.attrib[attribute_name]


    def iterate(self, xpath):
        try:
            for element in self.root.findall(self._uri(xpath)):
                yield XMLElementFacade(element, self.filename, self.namespace)
        except:
            logger.exception('error iterating through "%s" (file "%s")',
                    xpath, self.filename)
            raise


    def decimal(self, xpath, default=None, alternative_xpath=None):
        str_value = self.text(xpath,
                default=default, alternative_xpath=alternative_xpath)
        return Decimal(str_value)


    def _el(self, xpath):
        try:
            el = self.root.find(self._uri(xpath))
            return el
        except:
            logger.exception('error getting text for xpath: "%s" (file "%s")',
                    xpath, self.filename)
            raise XMLPathError(xpath)


    def _uri(self, xpath):
        if self.namespace is None:
            return xpath
        args = xpath.split('/')
        return '/'.join(['%s%s' % (self.namespace, arg) for arg in args])


class XMLFacadeFromString(XMLFacade):
    """Um façade para lidar com strings XML.

    .. sourcecode::

        >>> xml = XMLFacadeFromString('<example foo="bar"><a atag="tagA">A<b>B<c>C</c></b></a></example>')
        >>> xml.root_attr('foo')
        'bar'
        >>> xml.text('a')
        'A'
        >>> xml.attr('a', 'atag')
        'tagA'
        >>> xml.text('a/b')
        'B'
        >>> xml.text('a/b/c')
        'C'

    """

    def __init__(self, xmldata, namespace=None):
        self._xmldata = xmldata
        super(XMLFacadeFromString, self).__init__(':memory:',
                namespace=namespace)


    @property
    def xmldata(self):
        return self._xmldata


    def _begin_processing(self):
        try:
            self.tree = ET.fromstring(self._xmldata)
            self.root = self.tree # não há root de `fromstring`... já é root
            self.element = XMLElementFacade(
                    self.root, self.filename, self.namespace)
        except:
            logger.exception('error parsing XML from string')
            raise


    def done(self):
        pass
