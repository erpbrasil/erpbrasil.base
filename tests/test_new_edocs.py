# Copyright (C) 2024 Renato Lima
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from unittest import TestCase
from erpbrasil.base.fiscal.edoc import ChaveEdoc
from erpbrasil.base.fiscal.edoc import detectar_chave_edoc

class TestNewEdocs(TestCase):
    def test_nf3e_generate_and_validate(self):
        # NF3e - Model 66
        # cUF(2), AAMM(4), CNPJ(14), mod(2), serie(3), nNF(9), tpEmis(1), nSiteAutoriz(1), cNF3e(7), cDV(1)
        cnpj = "02.960.895/0001-31"
        ano_mes = "2401"
        codigo_uf = 35
        forma_emissao = "1"
        modelo_documento = "66"
        numero_documento = "123456789"
        numero_serie = "001"
        site_autorizador = "2"
        
        edoc = ChaveEdoc(
            codigo_uf=codigo_uf,
            ano_mes=ano_mes,
            cnpj_cpf_emitente=cnpj,
            modelo_documento=modelo_documento,
            numero_serie=numero_serie,
            numero_documento=numero_documento,
            forma_emissao=forma_emissao,
            site_autorizador=site_autorizador,
            validar=True
        )
        
        self.assertEqual(edoc.modelo_documento, "66")
        self.assertEqual(edoc.site_autorizador, "2")
        self.assertEqual(len(edoc.codigo_aleatorio), 7)
        self.assertEqual(len(edoc.chave), 44)
        
        # Test detection
        edoc_detected = detectar_chave_edoc(edoc.chave)
        self.assertEqual(edoc_detected.modelo_documento, "66")
        self.assertEqual(edoc_detected.site_autorizador, "2")

    def test_bpe_generate_and_validate(self):
        # BP-e - Model 63 (Standard structure)
        cnpj = "02.960.895/0001-31"
        ano_mes = "2401"
        codigo_uf = 35
        forma_emissao = "1"
        modelo_documento = "63"
        numero_documento = "123456789"
        numero_serie = "001"
        
        edoc = ChaveEdoc(
            codigo_uf=codigo_uf,
            ano_mes=ano_mes,
            cnpj_cpf_emitente=cnpj,
            modelo_documento=modelo_documento,
            numero_serie=numero_serie,
            numero_documento=numero_documento,
            forma_emissao=forma_emissao,
            validar=True
        )
        
        self.assertEqual(edoc.modelo_documento, "63")
        self.assertEqual(edoc.site_autorizador, False)
        self.assertEqual(len(edoc.codigo_aleatorio), 8)
        self.assertEqual(len(edoc.chave), 44)

    def test_nfcom_generate_and_validate(self):
        # NFCom - Model 62
        cnpj = "02.960.895/0001-31"
        ano_mes = "2401"
        codigo_uf = 35
        forma_emissao = "1"
        modelo_documento = "62"
        numero_documento = "123456789"
        numero_serie = "001"
        site_autorizador = "5"
        
        edoc = ChaveEdoc(
            codigo_uf=codigo_uf,
            ano_mes=ano_mes,
            cnpj_cpf_emitente=cnpj,
            modelo_documento=modelo_documento,
            numero_serie=numero_serie,
            numero_documento=numero_documento,
            forma_emissao=forma_emissao,
            site_autorizador=site_autorizador,
            validar=True
        )
        
        self.assertEqual(edoc.modelo_documento, "62")
        self.assertEqual(edoc.site_autorizador, "5")
        self.assertEqual(len(edoc.codigo_aleatorio), 7)

    def test_nfag_generate_and_validate(self):
        # NFAg - Model 75
        cnpj = "02.960.895/0001-31"
        ano_mes = "2401"
        codigo_uf = 35
        forma_emissao = "1"
        modelo_documento = "75"
        numero_documento = "123456789"
        numero_serie = "001"
        site_autorizador = "1"
        
        edoc = ChaveEdoc(
            codigo_uf=codigo_uf,
            ano_mes=ano_mes,
            cnpj_cpf_emitente=cnpj,
            modelo_documento=modelo_documento,
            numero_serie=numero_serie,
            numero_documento=numero_documento,
            forma_emissao=forma_emissao,
            site_autorizador=site_autorizador,
            validar=True
        )
        
        self.assertEqual(edoc.modelo_documento, "75")
        self.assertEqual(edoc.site_autorizador, "1")
        self.assertEqual(len(edoc.codigo_aleatorio), 7)

    def test_nfgas_generate_and_validate(self):
        # NFGas - Model 76
        cnpj = "02.960.895/0001-31"
        ano_mes = "2401"
        codigo_uf = 35
        forma_emissao = "1"
        modelo_documento = "76"
        numero_documento = "123456789"
        numero_serie = "001"
        site_autorizador = "1"
        
        edoc = ChaveEdoc(
            codigo_uf=codigo_uf,
            ano_mes=ano_mes,
            cnpj_cpf_emitente=cnpj,
            modelo_documento=modelo_documento,
            numero_serie=numero_serie,
            numero_documento=numero_documento,
            forma_emissao=forma_emissao,
            site_autorizador=site_autorizador,
            validar=True
        )
        
        self.assertEqual(edoc.modelo_documento, "76")
        self.assertEqual(edoc.site_autorizador, "1")
        self.assertEqual(len(edoc.codigo_aleatorio), 7)
