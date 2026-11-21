# Copyright (C) 2024 Renato Lima
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from unittest import TestCase

from erpbrasil.base.fiscal.edoc import ChaveEdoc, detectar_chave_edoc


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
            validar=True,
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
            validar=True,
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
            validar=True,
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
            validar=True,
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
            validar=True,
        )

        self.assertEqual(edoc.modelo_documento, "76")
        self.assertEqual(edoc.site_autorizador, "1")
        self.assertEqual(len(edoc.codigo_aleatorio), 7)

    def test_gtve_generate_and_validate(self):
        # GTV-e - Model 64 (Standard structure, CT-e family)
        edoc = ChaveEdoc(
            cUF=35,
            dhEmi="2611",
            CNPJ="02.960.895/0001-31",
            mod="64",
            serie="001",
            nNF="123456789",
            validar=True,
        )

        self.assertEqual(edoc.mod, "64")
        self.assertEqual(edoc.prefixo, "CTe")
        self.assertEqual(len(edoc.cNF), 8)
        self.assertFalse(edoc.nSiteAutoriz)
        self.assertEqual(detectar_chave_edoc(edoc.chave).mod, "64")

    def test_nfeabi_generate_and_validate(self):
        # NF-e ABI - Model 77
        # cUF(2), AAMM(4), CNPJ(14), mod(2), serie(3), nNF(9), tpEmis(1), nSiteAutoriz(1), cNF(7), cDV(1)
        edoc = ChaveEdoc(
            cUF=35,
            dhEmi="2611",
            CNPJ="02.960.895/0001-31",
            mod="77",
            serie="001",
            nNF="123456789",
            nSiteAutoriz="2",
            validar=True,
        )

        self.assertEqual(edoc.prefixo, "NFeABI")
        self.assertEqual(edoc.nSiteAutoriz, "2")
        self.assertEqual(len(edoc.cNF), 7)
        edoc_detected = detectar_chave_edoc(edoc.chave)
        self.assertEqual(edoc_detected.mod, "77")
        self.assertEqual(edoc_detected.nSiteAutoriz, "2")

    def test_dce_generate_and_validate(self):
        # DC-e - Model 99
        # cUF(2), AAMM(4), CNPJ(14), mod(2), serie(3), nDC(9), tpEmis(1), tpEmit(1), nSiteAutoriz(1), cDC(6), cDV(1)
        edoc = ChaveEdoc(
            cUF=35,
            dhEmi="2611",
            CNPJ="02.960.895/0001-31",
            mod="99",
            serie="001",
            nNF="123",
            tpEmit="2",
            nSiteAutoriz="0",
            cNF="482913",
            validar=True,
        )

        self.assertEqual(edoc.chave, "35261102960895000131990010000001231204829139")
        self.assertEqual(edoc.prefixo_chave, "DCe35261102960895000131990010000001231204829139")
        self.assertEqual(edoc.tpEmis, "1")
        self.assertEqual(edoc.tpEmit, "2")
        self.assertEqual(edoc.nSiteAutoriz, "0")
        self.assertEqual(edoc.cNF, "482913")

        edoc_detected = detectar_chave_edoc(edoc.chave)
        self.assertEqual(edoc_detected.tpEmit, "2")
        self.assertEqual(edoc_detected.cNF, "482913")

    def test_dce_random_code(self):
        edoc = ChaveEdoc(
            cUF=35,
            dhEmi="2611",
            CNPJ="02.960.895/0001-31",
            mod="99",
            serie="001",
            nNF="123",
            tpEmit=0,
            validar=True,
        )

        self.assertEqual(edoc.tpEmit, "0")
        self.assertEqual(edoc.nSiteAutoriz, "0")
        self.assertEqual(len(edoc.cNF), 6)
        self.assertEqual(len(edoc.chave), 44)

    def test_dce_requires_tp_emit(self):
        with self.assertRaises(ValueError):
            ChaveEdoc(
                cUF=35,
                dhEmi="2611",
                CNPJ="02.960.895/0001-31",
                mod="99",
                serie="001",
                nNF="123",
            )

    def test_tp_emit_only_dce(self):
        edoc = ChaveEdoc(chave="35210320695448000184550010000035891981839923", validar=True)
        self.assertFalse(edoc.tpEmit)
