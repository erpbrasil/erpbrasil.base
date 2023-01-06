# Copyright (C) 2020  Luis Felipe Mileo - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from unittest import TestCase

from erpbrasil.base.fiscal.edoc import ChaveCFeSAT
from erpbrasil.base.fiscal.edoc import ChaveEdoc
from erpbrasil.base.fiscal.edoc import detectar_chave_edoc


class Tests(TestCase):

    def test_mdfe_chave_objeto(self):
        cnpj = '48.740.351/0117-95'
        ano_mes = '1312'
        codigo_uf = 50
        forma_emissao = '1'
        modelo_documento = '58'
        numero_documento = '149000153'
        numero_serie = '000'
        chave = '50131248740351011795580001490001531345952745'
        edoc_1 = ChaveEdoc(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, 'Key: ano_mes failed')
        self.assertEqual(edoc_1.cnpj_cpf_emitente, cnpj, 'Key: cnpj_cpf_emitente failed')
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, 'Key: codigo_uf failed')
        self.assertEqual(edoc_1.forma_emissao, forma_emissao, 'Key: forma_emissao failed')
        self.assertEqual(edoc_1.modelo_documento, modelo_documento, 'Key: modelo_documento failed')
        self.assertEqual(edoc_1.numero_documento, numero_documento, 'Key: numero_documento failed')
        self.assertEqual(edoc_1.numero_serie, numero_serie, 'Key: numero_serie failed')

        self.assertEqual(edoc_1.ano_emissao, 2013, 'Key: ano_emissao failed')
        self.assertEqual(edoc_1.codigo_aleatorio, '34595274', 'Key: codigo_aleatorio failed')
        self.assertEqual(edoc_1.digito_verificador, '5', 'Key: digito_verificador failed')
        self.assertEqual(edoc_1.mes_emissao, 12, 'Key: mes_emissao failed')

        edoc_2 = ChaveEdoc(
            ano_mes=ano_mes,
            cnpj_cpf_emitente=cnpj,
            codigo_uf=codigo_uf,
            forma_emissao=forma_emissao,
            modelo_documento=modelo_documento,
            numero_documento=numero_documento,
            numero_serie=numero_serie,
        )

        self.assertEqual(chave, edoc_2.chave)
        self.assertEqual(edoc_1.chave, chave)

        self.assertEqual(
            edoc_1.partes(),
            edoc_2.partes(),
            'Key: partes failed'
        )

    def test_cte_chave_objeto(self):
        cnpj = '32.438.772/0001-04'
        ano_mes = '1712'
        codigo_uf = 32
        forma_emissao = '1'
        modelo_documento = '57'
        numero_documento = '000199075'
        numero_serie = '001'

        chave = '32171232438772000104570010001990751153183825'
        edoc_1 = ChaveEdoc(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, 'Key: ano_mes failed')
        self.assertEqual(edoc_1.cnpj_cpf_emitente, cnpj, 'Key: cnpj_cpf_emitente failed')
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, 'Key: codigo_uf failed')
        self.assertEqual(edoc_1.forma_emissao, forma_emissao, 'Key: forma_emissao failed')
        self.assertEqual(edoc_1.modelo_documento, modelo_documento, 'Key: modelo_documento failed')
        self.assertEqual(edoc_1.numero_documento, numero_documento, 'Key: numero_documento failed')
        self.assertEqual(edoc_1.numero_serie, numero_serie, 'Key: numero_serie failed')

        self.assertEqual(edoc_1.ano_emissao, 2017, 'Key: ano_emissao failed')
        self.assertEqual(edoc_1.codigo_aleatorio, '15318382', 'Key: codigo_aleatorio failed')
        self.assertEqual(edoc_1.digito_verificador, '5', 'Key: digito_verificador failed')
        self.assertEqual(edoc_1.mes_emissao, 12, 'Key: mes_emissao failed')

        edoc_2 = ChaveEdoc(
            ano_mes=ano_mes,
            cnpj_cpf_emitente=cnpj,
            codigo_uf=codigo_uf,
            forma_emissao=forma_emissao,
            modelo_documento=modelo_documento,
            numero_documento=numero_documento,
            numero_serie=numero_serie,
        )

        self.assertEqual(chave, edoc_2.chave)
        self.assertEqual(edoc_1.chave, chave)

        self.assertEqual(
            edoc_1.partes(),
            edoc_2.partes(),
            'Key: partes failed'
        )

    def test_nfce_chave_objeto(self):
        cnpj = '01.098.983/0106-80'
        ano_mes = '1402'
        codigo_uf = 43
        forma_emissao = '1'
        modelo_documento = '65'
        numero_documento = '000000599'
        numero_serie = '796'

        chave = '43140201098983010680657960000005991148127446'
        edoc_1 = ChaveEdoc(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, 'Key: ano_mes failed')
        self.assertEqual(edoc_1.cnpj_cpf_emitente, cnpj, 'Key: cnpj_cpf_emitente failed')
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, 'Key: codigo_uf failed')
        self.assertEqual(edoc_1.forma_emissao, forma_emissao, 'Key: forma_emissao failed')
        self.assertEqual(edoc_1.modelo_documento, modelo_documento, 'Key: modelo_documento failed')
        self.assertEqual(edoc_1.numero_documento, numero_documento, 'Key: numero_documento failed')
        self.assertEqual(edoc_1.numero_serie, numero_serie, 'Key: numero_serie failed')

        self.assertEqual(edoc_1.ano_emissao, 2014, 'Key: ano_emissao failed')
        self.assertEqual(edoc_1.codigo_aleatorio, '14812744', 'Key: codigo_aleatorio failed')
        self.assertEqual(edoc_1.digito_verificador, '6', 'Key: digito_verificador failed')
        self.assertEqual(edoc_1.mes_emissao, 2, 'Key: mes_emissao failed')

        edoc_2 = ChaveEdoc(
            ano_mes=ano_mes,
            cnpj_cpf_emitente=cnpj,
            codigo_uf=codigo_uf,
            forma_emissao=forma_emissao,
            modelo_documento=modelo_documento,
            numero_documento=numero_documento,
            numero_serie=numero_serie,
        )

        self.assertEqual(chave, edoc_2.chave)
        self.assertEqual(edoc_1.chave, chave)

        self.assertEqual(
            edoc_1.partes(),
            edoc_2.partes(),
            'Key: partes failed'
        )

    def test_nfe_chave_objeto(self):
        cnpj = '20.695.448/0001-84'
        ano_mes = '2103'
        codigo_uf = 35
        forma_emissao = '1'
        modelo_documento = '55'
        numero_documento = '000003589'
        numero_serie = '001'

        chave = '35210320695448000184550010000035891981839923'
        edoc_1 = ChaveEdoc(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, 'Key: ano_mes failed')
        self.assertEqual(edoc_1.cnpj_cpf_emitente, cnpj, 'Key: cnpj_cpf_emitente failed')
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, 'Key: codigo_uf failed')
        self.assertEqual(edoc_1.forma_emissao, forma_emissao, 'Key: forma_emissao failed')
        self.assertEqual(edoc_1.modelo_documento, modelo_documento, 'Key: modelo_documento failed')
        self.assertEqual(edoc_1.numero_documento, numero_documento, 'Key: numero_documento failed')
        self.assertEqual(edoc_1.numero_serie, numero_serie, 'Key: numero_serie failed')

        self.assertEqual(edoc_1.ano_emissao, 2021, 'Key: ano_emissao failed')
        self.assertEqual(edoc_1.codigo_aleatorio, '98183992', 'Key: codigo_aleatorio failed')
        self.assertEqual(edoc_1.digito_verificador, '3', 'Key: digito_verificador failed')
        self.assertEqual(edoc_1.mes_emissao, 3, 'Key: mes_emissao failed')

        edoc_2 = ChaveEdoc(
            ano_mes=ano_mes,
            cnpj_cpf_emitente=cnpj,
            codigo_uf=codigo_uf,
            forma_emissao=forma_emissao,
            modelo_documento=modelo_documento,
            numero_documento=numero_documento,
            numero_serie=numero_serie,
        )

        self.assertEqual(chave, edoc_2.chave)
        self.assertEqual(edoc_1.chave, chave)

        self.assertEqual(
            edoc_1.partes(),
            edoc_2.partes(),
            'Key: partes failed'
        )

    def test_nfe_prefixo_chave_objeto(self):
        cnpj = '20.695.448/0001-84'
        ano_mes = '2103'
        codigo_uf = 35
        forma_emissao = '1'
        modelo_documento = '55'
        numero_documento = '000003589'
        numero_serie = '001'

        chave = '35210320695448000184550010000035891981839923'
        edoc_1 = ChaveEdoc(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, 'Key: ano_mes failed')
        self.assertEqual(edoc_1.cnpj_cpf_emitente, cnpj, 'Key: cnpj_cpf_emitente failed')
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, 'Key: codigo_uf failed')
        self.assertEqual(edoc_1.forma_emissao, forma_emissao, 'Key: forma_emissao failed')
        self.assertEqual(edoc_1.modelo_documento, modelo_documento, 'Key: modelo_documento failed')
        self.assertEqual(edoc_1.numero_documento, numero_documento, 'Key: numero_documento failed')
        self.assertEqual(edoc_1.numero_serie, numero_serie, 'Key: numero_serie failed')

        self.assertEqual(edoc_1.ano_emissao, 2021, 'Key: ano_emissao failed')
        self.assertEqual(edoc_1.codigo_aleatorio, '98183992', 'Key: codigo_aleatorio failed')
        self.assertEqual(edoc_1.digito_verificador, '3', 'Key: digito_verificador failed')
        self.assertEqual(edoc_1.mes_emissao, 3, 'Key: mes_emissao failed')

        edoc_2 = ChaveEdoc(
            ano_mes=ano_mes,
            cnpj_cpf_emitente=cnpj,
            codigo_uf=codigo_uf,
            forma_emissao=forma_emissao,
            modelo_documento=modelo_documento,
            numero_documento=numero_documento,
            numero_serie=numero_serie,
        )

        self.assertEqual(chave, edoc_2.chave)
        self.assertEqual(edoc_1.chave, chave)
        self.assertEqual(edoc_1.prefixo_chave, edoc_2.prefixo_chave)

        self.assertEqual(
            edoc_1.partes(),
            edoc_2.partes(),
            'Key: partes failed'
        )

    def test_cfe_chave_objeto(self):
        cnpj = '08.723.218/0001-86'
        ano_mes = '1508'
        codigo_uf = 35
        forma_emissao = ''
        modelo_documento = '59'
        numero_documento = '000055'
        numero_serie = '900004019'

        chave = '35150808723218000186599000040190000557255950'
        edoc_1 = ChaveCFeSAT(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, 'Key: ano_mes failed')
        self.assertEqual(edoc_1.cnpj_cpf_emitente, cnpj, 'Key: cnpj_cpf_emitente failed')
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, 'Key: codigo_uf failed')
        self.assertEqual(edoc_1.forma_emissao, forma_emissao, 'Key: forma_emissao failed')
        self.assertEqual(edoc_1.modelo_documento, modelo_documento, 'Key: modelo_documento failed')
        self.assertEqual(edoc_1.numero_documento, numero_documento, 'Key: numero_documento failed')
        self.assertEqual(edoc_1.numero_serie, numero_serie, 'Key: numero_serie failed')

        self.assertEqual(edoc_1.codigo_aleatorio, '725595', 'Key: codigo_aleatorio failed')
        self.assertEqual(edoc_1.ano_emissao, 2015, 'Key: ano_emissao failed')
        self.assertEqual(edoc_1.digito_verificador, '0', 'Key: digito_verificador failed')
        self.assertEqual(edoc_1.mes_emissao, 8, 'Key: mes_emissao failed')

        self.assertEqual(edoc_1.chave, chave)

        self.assertEqual(
            edoc_1.partes(),
            ['3515', '0808', '7232', '1800', '0186', '5990', '0004', '0190', '0005', '5725', '5950'],
            'Key: partes failed'
        )

    def test_cfe2_chave_objeto(self):
        cnpj = '08.723.218/0001-86'
        ano_mes = '1508'
        codigo_uf = 35
        forma_emissao = ''
        modelo_documento = '59'
        numero_documento = '000024'
        numero_serie = '900004019'

        chave = '35150808723218000186599000040190000241114257'
        edoc_1 = ChaveCFeSAT(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, 'Key: ano_mes failed')
        self.assertEqual(edoc_1.cnpj_cpf_emitente, cnpj, 'Key: cnpj_cpf_emitente failed')
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, 'Key: codigo_uf failed')
        self.assertEqual(edoc_1.forma_emissao, forma_emissao, 'Key: forma_emissao failed')
        self.assertEqual(edoc_1.modelo_documento, modelo_documento, 'Key: modelo_documento failed')
        self.assertEqual(edoc_1.numero_documento, numero_documento, 'Key: numero_documento failed')
        self.assertEqual(edoc_1.numero_serie, numero_serie, 'Key: numero_serie failed')

        self.assertEqual(edoc_1.ano_emissao, 2015, 'Key: ano_emissao failed')
        self.assertEqual(edoc_1.codigo_aleatorio, '111425', 'Key: codigo_aleatorio failed')
        self.assertEqual(edoc_1.digito_verificador, '7', 'Key: digito_verificador failed')
        self.assertEqual(edoc_1.mes_emissao, 8, 'Key: mes_emissao failed')

        self.assertEqual(edoc_1.chave, chave)

        self.assertEqual(
            edoc_1.partes(),
            ['3515', '0808', '7232', '1800', '0186', '5990', '0004', '0190', '0002', '4111', '4257'],
            'Key: partes failed'
        )

    def test_invalid_key(self):

        chaves_invalidas = [
            # número do CNPJ emitente inválido
            '35150808723218000187599000040190000241114259',

            # NF-E
            '35210320695448000184550010000035891981839924',
            # Modelo invalido - 54
            '35210320695448000184540010000035891981839924',
            # NFE em maiusculo
            '35210320695448000184540010000035891981839924',
            # UF Inválida
            '99150808723218000186599000040190000241114257',
            # Chave com série de CNPJ mas com CPF emitente
            '42221200050690671849558890000000811540256167',

        ]
        for chave in chaves_invalidas:
            with self.assertRaises(ValueError):
                detectar_chave_edoc(chave=chave)

    def test_valid_key(self):

        chaves_validas = [
            '50131248740351011795580001490001531345952745',
            '43140201098983010680657960000005991148127446',
            '35210320695448000184550010000035891981839923',
            '32171232438772000104570010001990751153183825',
            '35150808723218000186599000040190000241114257',
            '35150808723218000186599000040190000557255950',
            '42221200050690671849559100000000811540256167',
        ]
        for chave in chaves_validas:
            edoc = detectar_chave_edoc(chave=chave)
            self.assertTrue(edoc, 'Erro chave edoc')
