# Copyright (C) 2020  Luis Felipe Mileo - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from unittest import TestCase

from erpbrasil.base.fiscal.chave import ChaveEdoc


class Tests(TestCase):

    def test_mdfe_chave_objeto(self):
        mdfe = ChaveEdoc(chave='MDFe50131248740351011795580001490001531162619648')
        self.assertEqual(mdfe.ano_emissao, 2013, 'Key: ano_emissao failed')
        self.assertEqual(mdfe.ano_mes, '1312', 'Key: ano_mes failed')
        self.assertEqual(
            mdfe.cnpj_emitente, '48.740.351/0117-95', 'Key: cnpj_emitente failed')
        self.assertEqual(mdfe.codigo_aleatorio, '116261964', 'Key: codigo_aleatorio failed')
        self.assertEqual(mdfe.codigo_uf, 50, 'Key: codigo_uf failed')
        self.assertEqual(mdfe.digito_verificador, '8', 'Key: digito_verificador failed')
        self.assertEqual(mdfe.forma_emissao, '3', 'Key: forma_emissao failed')
        self.assertEqual(mdfe.mes_emissao, 12, 'Key: mes_emissao failed')
        self.assertEqual(mdfe.modelo_documento, '58', 'Key: modelo_documento failed')
        self.assertEqual(mdfe.numero_documento, '014900015', 'Key: numero_documento failed')
        self.assertEqual(mdfe.numero_serie, '00', 'Key: numero_serie failed')
        self.assertEqual(
            mdfe.partes(),
            ['5013', '1248', '7403', '5101', '1795', '5800', '0149', '0001', '5311', '6261', '9648'],
            'Key: partes failed'
        )

    def test_cte_chave_objeto(self):
        cte = ChaveEdoc(chave='CTe32171232438772000104570010001990751398682263')

        self.assertEqual(cte.ano_emissao, 2017, 'Key: ano_emissao failed')
        self.assertEqual(cte.ano_mes, '1712', 'Key: ano_mes failed')
        self.assertEqual(
            cte.cnpj_emitente, '32.438.772/0001-04', 'Key: cnpj_emitente failed')
        self.assertEqual(cte.codigo_aleatorio, '139868226', 'Key: codigo_aleatorio failed')
        self.assertEqual(cte.codigo_uf, 32, 'Key: codigo_uf failed')
        self.assertEqual(cte.digito_verificador, '3', 'Key: digito_verificador failed')
        self.assertEqual(cte.forma_emissao, '5', 'Key: forma_emissao failed')
        self.assertEqual(cte.mes_emissao, 12, 'Key: mes_emissao failed')
        self.assertEqual(cte.modelo_documento, '57', 'Key: modelo_documento failed')
        self.assertEqual(cte.numero_documento, '100019907', 'Key: numero_documento failed')
        self.assertEqual(cte.numero_serie, '00', 'Key: numero_serie failed')
        self.assertEqual(
            cte.partes(),
            ['3217', '1232', '4387', '7200', '0104', '5700', '1000', '1990', '7513', '9868', '2263'],
            'Key: partes failed'
        )

    def test_nfce_chave_objeto(self):
        nfce = ChaveEdoc(chave='NFe43140201098983010680657960000005991314477464')

        self.assertEqual(nfce.ano_emissao, 2014, 'Key: ano_emissao failed')
        self.assertEqual(nfce.ano_mes, '1402', 'Key: ano_mes failed')
        self.assertEqual(
            nfce.cnpj_emitente, '01.098.983/0106-80', 'Key: cnpj_emitente failed')
        self.assertEqual(nfce.codigo_aleatorio, '131447746', 'Key: codigo_aleatorio failed')
        self.assertEqual(nfce.codigo_uf, 43, 'Key: codigo_uf failed')
        self.assertEqual(nfce.digito_verificador, '4', 'Key: digito_verificador failed')
        self.assertEqual(nfce.forma_emissao, '9', 'Key: forma_emissao failed')
        self.assertEqual(nfce.mes_emissao, 2, 'Key: mes_emissao failed')
        self.assertEqual(nfce.modelo_documento, '65', 'Key: modelo_documento failed')
        self.assertEqual(nfce.numero_documento, '600000059', 'Key: numero_documento failed')
        self.assertEqual(nfce.numero_serie, '79', 'Key: numero_serie failed')
        self.assertEqual(
            nfce.partes(),
            ['4314', '0201', '0989', '8301', '0680', '6579', '6000', '0005', '9913', '1447', '7464'],
            'Key: partes failed'
        )

    def test_cfe_chave_objeto(self):
        cfe = ChaveEdoc(chave='CFe35150808723218000186599000040190000241114257')

        self.assertEqual(cfe.ano_emissao, 2015, 'Key: ano_emissao failed')
        self.assertEqual(cfe.ano_mes, '1508', 'Key: ano_mes failed')
        self.assertEqual(
            cfe.cnpj_emitente, '08.723.218/0001-86', 'Key: cnpj_emitente failed')
        self.assertEqual(cfe.codigo_aleatorio, '024111425', 'Key: codigo_aleatorio failed')
        self.assertEqual(cfe.codigo_uf, 35, 'Key: codigo_uf failed')
        self.assertEqual(cfe.digito_verificador, '7', 'Key: digito_verificador failed')
        self.assertEqual(cfe.forma_emissao, '0', 'Key: forma_emissao failed')
        self.assertEqual(cfe.mes_emissao, 8, 'Key: mes_emissao failed')
        self.assertEqual(cfe.modelo_documento, '59', 'Key: modelo_documento failed')
        self.assertEqual(cfe.numero_documento, '000401900', 'Key: numero_documento failed')
        self.assertEqual(cfe.numero_serie, '90', 'Key: numero_serie failed')
        self.assertEqual(
            cfe.partes(),
            ['3515', '0808', '7232', '1800', '0186', '5990', '0004', '0190', '0002', '4111', '4257'],
            'Key: partes failed'
        )


    # def test_cte_objeto_chave(self):
        # cte = ChaveEdoc()
        # cte.ano_emissao = 2017
        # cte.ano_mes = '1712'
        # cte.cnpj_emitente = '32.438.772/0001-04'
        # cte.codigo_aleatorio = '139868226'
        # cte.codigo_uf = 32
        # cte.digito_verificador = '3'
        # cte.forma_emissao = '5'
        # cte.mes_emissao = 12
        # cte.modelo_documento = '57'
        # cte.numero_documento = '100019907'
        # cte.numero_serie = '00'
