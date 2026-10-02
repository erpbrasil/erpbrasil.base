# Copyright (C) 2020  Luis Felipe Mileo - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from unittest import TestCase

from erpbrasil.base.fiscal.edoc import ChaveCFeSAT
from erpbrasil.base.fiscal.edoc import ChaveEdoc
from erpbrasil.base.fiscal.edoc import detectar_chave_edoc
from erpbrasil.base.misc import modulo11


class Tests(TestCase):
    def test_mdfe_chave_objeto(self):
        cnpj = "48.740.351/0117-95"
        ano_mes = "1312"
        codigo_uf = 50
        forma_emissao = "1"
        modelo_documento = "58"
        numero_documento = "149000153"
        numero_serie = "000"
        chave = "50131248740351011795580001490001531345952745"
        edoc_1 = ChaveEdoc(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, "Key: ano_mes failed")
        self.assertEqual(
            edoc_1.cnpj_cpf_emitente, cnpj, "Key: cnpj_cpf_emitente failed"
        )
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, "Key: codigo_uf failed")
        self.assertEqual(
            edoc_1.forma_emissao, forma_emissao, "Key: forma_emissao failed"
        )
        self.assertEqual(
            edoc_1.modelo_documento, modelo_documento, "Key: modelo_documento failed"
        )
        self.assertEqual(
            edoc_1.numero_documento, numero_documento, "Key: numero_documento failed"
        )
        self.assertEqual(edoc_1.numero_serie, numero_serie, "Key: numero_serie failed")

        self.assertEqual(edoc_1.ano_emissao, 2013, "Key: ano_emissao failed")
        self.assertEqual(
            edoc_1.codigo_aleatorio, "34595274", "Key: codigo_aleatorio failed"
        )
        self.assertEqual(
            edoc_1.digito_verificador, "5", "Key: digito_verificador failed"
        )
        self.assertEqual(edoc_1.mes_emissao, 12, "Key: mes_emissao failed")

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

        self.assertEqual(edoc_1.partes(), edoc_2.partes(), "Key: partes failed")

    def test_cte_chave_objeto(self):
        cnpj = "32.438.772/0001-04"
        ano_mes = "1712"
        codigo_uf = 32
        forma_emissao = "1"
        modelo_documento = "57"
        numero_documento = "000199075"
        numero_serie = "001"

        chave = "32171232438772000104570010001990751153183825"
        edoc_1 = ChaveEdoc(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, "Key: ano_mes failed")
        self.assertEqual(
            edoc_1.cnpj_cpf_emitente, cnpj, "Key: cnpj_cpf_emitente failed"
        )
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, "Key: codigo_uf failed")
        self.assertEqual(
            edoc_1.forma_emissao, forma_emissao, "Key: forma_emissao failed"
        )
        self.assertEqual(
            edoc_1.modelo_documento, modelo_documento, "Key: modelo_documento failed"
        )
        self.assertEqual(
            edoc_1.numero_documento, numero_documento, "Key: numero_documento failed"
        )
        self.assertEqual(edoc_1.numero_serie, numero_serie, "Key: numero_serie failed")

        self.assertEqual(edoc_1.ano_emissao, 2017, "Key: ano_emissao failed")
        self.assertEqual(
            edoc_1.codigo_aleatorio, "15318382", "Key: codigo_aleatorio failed"
        )
        self.assertEqual(
            edoc_1.digito_verificador, "5", "Key: digito_verificador failed"
        )
        self.assertEqual(edoc_1.mes_emissao, 12, "Key: mes_emissao failed")

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

        self.assertEqual(edoc_1.partes(), edoc_2.partes(), "Key: partes failed")

    def test_nfce_chave_objeto(self):
        cnpj = "01.098.983/0106-80"
        ano_mes = "1402"
        codigo_uf = 43
        forma_emissao = "1"
        modelo_documento = "65"
        numero_documento = "000000599"
        numero_serie = "796"

        chave = "43140201098983010680657960000005991148127446"
        edoc_1 = ChaveEdoc(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, "Key: ano_mes failed")
        self.assertEqual(
            edoc_1.cnpj_cpf_emitente, cnpj, "Key: cnpj_cpf_emitente failed"
        )
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, "Key: codigo_uf failed")
        self.assertEqual(
            edoc_1.forma_emissao, forma_emissao, "Key: forma_emissao failed"
        )
        self.assertEqual(
            edoc_1.modelo_documento, modelo_documento, "Key: modelo_documento failed"
        )
        self.assertEqual(
            edoc_1.numero_documento, numero_documento, "Key: numero_documento failed"
        )
        self.assertEqual(edoc_1.numero_serie, numero_serie, "Key: numero_serie failed")

        self.assertEqual(edoc_1.ano_emissao, 2014, "Key: ano_emissao failed")
        self.assertEqual(
            edoc_1.codigo_aleatorio, "14812744", "Key: codigo_aleatorio failed"
        )
        self.assertEqual(
            edoc_1.digito_verificador, "6", "Key: digito_verificador failed"
        )
        self.assertEqual(edoc_1.mes_emissao, 2, "Key: mes_emissao failed")

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

        self.assertEqual(edoc_1.partes(), edoc_2.partes(), "Key: partes failed")

    def test_nfe_chave_objeto(self):
        cnpj = "20.695.448/0001-84"
        ano_mes = "2103"
        codigo_uf = 35
        forma_emissao = "1"
        modelo_documento = "55"
        numero_documento = "000003589"
        numero_serie = "001"

        chave = "35210320695448000184550010000035891981839923"
        edoc_1 = ChaveEdoc(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, "Key: ano_mes failed")
        self.assertEqual(
            edoc_1.cnpj_cpf_emitente, cnpj, "Key: cnpj_cpf_emitente failed"
        )
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, "Key: codigo_uf failed")
        self.assertEqual(
            edoc_1.forma_emissao, forma_emissao, "Key: forma_emissao failed"
        )
        self.assertEqual(
            edoc_1.modelo_documento, modelo_documento, "Key: modelo_documento failed"
        )
        self.assertEqual(
            edoc_1.numero_documento, numero_documento, "Key: numero_documento failed"
        )
        self.assertEqual(edoc_1.numero_serie, numero_serie, "Key: numero_serie failed")

        self.assertEqual(edoc_1.ano_emissao, 2021, "Key: ano_emissao failed")
        self.assertEqual(
            edoc_1.codigo_aleatorio, "98183992", "Key: codigo_aleatorio failed"
        )
        self.assertEqual(
            edoc_1.digito_verificador, "3", "Key: digito_verificador failed"
        )
        self.assertEqual(edoc_1.mes_emissao, 3, "Key: mes_emissao failed")

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

        self.assertEqual(edoc_1.partes(), edoc_2.partes(), "Key: partes failed")

    def test_nfe_prefixo_chave_objeto(self):
        cnpj = "20.695.448/0001-84"
        ano_mes = "2103"
        codigo_uf = 35
        forma_emissao = "1"
        modelo_documento = "55"
        numero_documento = "000003589"
        numero_serie = "001"

        chave = "35210320695448000184550010000035891981839923"
        edoc_1 = ChaveEdoc(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, "Key: ano_mes failed")
        self.assertEqual(
            edoc_1.cnpj_cpf_emitente, cnpj, "Key: cnpj_cpf_emitente failed"
        )
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, "Key: codigo_uf failed")
        self.assertEqual(
            edoc_1.forma_emissao, forma_emissao, "Key: forma_emissao failed"
        )
        self.assertEqual(
            edoc_1.modelo_documento, modelo_documento, "Key: modelo_documento failed"
        )
        self.assertEqual(
            edoc_1.numero_documento, numero_documento, "Key: numero_documento failed"
        )
        self.assertEqual(edoc_1.numero_serie, numero_serie, "Key: numero_serie failed")

        self.assertEqual(edoc_1.ano_emissao, 2021, "Key: ano_emissao failed")
        self.assertEqual(
            edoc_1.codigo_aleatorio, "98183992", "Key: codigo_aleatorio failed"
        )
        self.assertEqual(
            edoc_1.digito_verificador, "3", "Key: digito_verificador failed"
        )
        self.assertEqual(edoc_1.mes_emissao, 3, "Key: mes_emissao failed")

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

        self.assertEqual(edoc_1.partes(), edoc_2.partes(), "Key: partes failed")

    def test_cfe_chave_objeto(self):
        cnpj = "08.723.218/0001-86"
        ano_mes = "1508"
        codigo_uf = 35
        forma_emissao = ""
        modelo_documento = "59"
        numero_documento = "000055"
        numero_serie = "900004019"

        chave = "35150808723218000186599000040190000557255950"
        edoc_1 = ChaveCFeSAT(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, "Key: ano_mes failed")
        self.assertEqual(
            edoc_1.cnpj_cpf_emitente, cnpj, "Key: cnpj_cpf_emitente failed"
        )
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, "Key: codigo_uf failed")
        self.assertEqual(
            edoc_1.forma_emissao, forma_emissao, "Key: forma_emissao failed"
        )
        self.assertEqual(
            edoc_1.modelo_documento, modelo_documento, "Key: modelo_documento failed"
        )
        self.assertEqual(
            edoc_1.numero_documento, numero_documento, "Key: numero_documento failed"
        )
        self.assertEqual(edoc_1.numero_serie, numero_serie, "Key: numero_serie failed")

        self.assertEqual(
            edoc_1.codigo_aleatorio, "725595", "Key: codigo_aleatorio failed"
        )
        self.assertEqual(edoc_1.ano_emissao, 2015, "Key: ano_emissao failed")
        self.assertEqual(
            edoc_1.digito_verificador, "0", "Key: digito_verificador failed"
        )
        self.assertEqual(edoc_1.mes_emissao, 8, "Key: mes_emissao failed")

        self.assertEqual(edoc_1.chave, chave)

        self.assertEqual(
            edoc_1.partes(),
            [
                "3515",
                "0808",
                "7232",
                "1800",
                "0186",
                "5990",
                "0004",
                "0190",
                "0005",
                "5725",
                "5950",
            ],
            "Key: partes failed",
        )

    def test_cfe2_chave_objeto(self):
        cnpj = "08.723.218/0001-86"
        ano_mes = "1508"
        codigo_uf = 35
        forma_emissao = ""
        modelo_documento = "59"
        numero_documento = "000024"
        numero_serie = "900004019"

        chave = "35150808723218000186599000040190000241114257"
        edoc_1 = ChaveCFeSAT(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, "Key: ano_mes failed")
        self.assertEqual(
            edoc_1.cnpj_cpf_emitente, cnpj, "Key: cnpj_cpf_emitente failed"
        )
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, "Key: codigo_uf failed")
        self.assertEqual(
            edoc_1.forma_emissao, forma_emissao, "Key: forma_emissao failed"
        )
        self.assertEqual(
            edoc_1.modelo_documento, modelo_documento, "Key: modelo_documento failed"
        )
        self.assertEqual(
            edoc_1.numero_documento, numero_documento, "Key: numero_documento failed"
        )
        self.assertEqual(edoc_1.numero_serie, numero_serie, "Key: numero_serie failed")

        self.assertEqual(edoc_1.ano_emissao, 2015, "Key: ano_emissao failed")
        self.assertEqual(
            edoc_1.codigo_aleatorio, "111425", "Key: codigo_aleatorio failed"
        )
        self.assertEqual(
            edoc_1.digito_verificador, "7", "Key: digito_verificador failed"
        )
        self.assertEqual(edoc_1.mes_emissao, 8, "Key: mes_emissao failed")

        self.assertEqual(edoc_1.chave, chave)

        self.assertEqual(
            edoc_1.partes(),
            [
                "3515",
                "0808",
                "7232",
                "1800",
                "0186",
                "5990",
                "0004",
                "0190",
                "0002",
                "4111",
                "4257",
            ],
            "Key: partes failed",
        )

    def test_cte_os_chave_objeto(self):
        cnpj = "32.438.772/0001-04"
        ano_mes = "1712"
        codigo_uf = 32
        forma_emissao = "1"
        modelo_documento = "67"
        numero_documento = "000199075"
        numero_serie = "001"

        chave = "32171232438772000104670010001990751234429533"
        edoc_1 = ChaveEdoc(chave=chave)

        self.assertEqual(edoc_1.ano_mes, ano_mes, "Key: ano_mes failed")
        self.assertEqual(
            edoc_1.cnpj_cpf_emitente, cnpj, "Key: cnpj_cpf_emitente failed"
        )
        self.assertEqual(edoc_1.codigo_uf, codigo_uf, "Key: codigo_uf failed")
        self.assertEqual(
            edoc_1.forma_emissao, forma_emissao, "Key: forma_emissao failed"
        )
        self.assertEqual(
            edoc_1.modelo_documento, modelo_documento, "Key: modelo_documento failed"
        )
        self.assertEqual(
            edoc_1.numero_documento, numero_documento, "Key: numero_documento failed"
        )
        self.assertEqual(edoc_1.numero_serie, numero_serie, "Key: numero_serie failed")

        self.assertEqual(edoc_1.ano_emissao, 2017, "Key: ano_emissao failed")
        self.assertEqual(
            edoc_1.codigo_aleatorio, "23442953", "Key: codigo_aleatorio failed"
        )
        self.assertEqual(
            edoc_1.digito_verificador, "3", "Key: digito_verificador failed"
        )
        self.assertEqual(edoc_1.mes_emissao, 12, "Key: mes_emissao failed")

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

        self.assertEqual(edoc_1.partes(), edoc_2.partes(), "Key: partes failed")

    def test_invalid_key(self):
        chaves_invalidas = [
            # número do CNPJ emitente inválido
            "35150808723218000187599000040190000241114259",
            # NF-E
            "35210320695448000184550010000035891981839924",
            # Modelo invalido - 54
            "35210320695448000184540010000035891981839924",
            # NFE em maiusculo
            "35210320695448000184540010000035891981839924",
            # UF Inválida
            "99150808723218000186599000040190000241114257",
            # Chave com série de CNPJ mas com CPF emitente
            "42221200050690671849558890000000811540256167",
        ]
        for chave in chaves_invalidas:
            with self.assertRaises(ValueError):
                detectar_chave_edoc(chave=chave)

    def test_valid_key(self):
        chaves_validas = [
            "50131248740351011795580001490001531345952745",
            "43140201098983010680657960000005991148127446",
            "35210320695448000184550010000035891981839923",
            "32171232438772000104570010001990751153183825",
            "35150808723218000186599000040190000241114257",
            "35150808723218000186599000040190000557255950",
            "42221200050690671849559100000000811540256167",
            "32171232438772000104670010001990751234429533",
        ]
        for chave in chaves_validas:
            edoc = detectar_chave_edoc(chave=chave)
            self.assertTrue(edoc, "Erro chave edoc")


class TestChaveCNPJAlfanumerico(TestCase):
    """Chave de acesso com CNPJ alfanumerico.

    NT Conjunta 2025.001 v1.00, item 5: a chave segue a expressao
    [0-9]{6}[A-Z0-9]{12}[0-9]{26} e o DV e o modulo 11 sobre o valor
    ASCII - 48 de cada caractere (Anexo II). As chaves abaixo foram
    calculadas com um porte direto do Anexo II, sem usar a biblioteca.
    """

    CNPJ_ALFA = "12.ABC.345/01DE-35"  # exemplo do Perguntas e Respostas da RFB

    CHAVES_ALFA = {
        "55": "35260712ABC34501DE35550010000001231754505705",
        "57": "41260812IBC34D000140570010000045671843096443",
        "65": "43260712ABC34501DE35650020000000101818644767",
        "58": "50260912OBC34D000181580000000007771603323854",
        "59": "35260712ABC34501DE35599000040190000551234564",
    }

    @staticmethod
    def _troca(chave, posicao, caractere):
        """Troca um caractere e recalcula o DV, para que a recusa venha da
        posicao do caractere e nao do DV."""
        base = chave[:posicao] + caractere + chave[posicao + 1 : 43]
        return base + str(modulo11(base))

    def test_chaves_alfa_validas(self):
        for modelo, chave in self.CHAVES_ALFA.items():
            with self.subTest(modelo=modelo):
                edoc = detectar_chave_edoc(chave)
                self.assertEqual(edoc.chave, chave)
                self.assertEqual(edoc.modelo_documento, modelo)
                self.assertEqual(edoc.digito_verificador, chave[-1])

    def test_chave_alfa_campos(self):
        edoc = ChaveEdoc(chave=self.CHAVES_ALFA["55"], validar=True)
        self.assertEqual(edoc.cnpj_cpf_emitente, self.CNPJ_ALFA)
        self.assertEqual(edoc.codigo_uf, 35)
        self.assertEqual(edoc.ano_emissao, 2026)
        self.assertEqual(edoc.mes_emissao, 7)
        self.assertEqual(edoc.numero_serie, "001")
        self.assertEqual(edoc.numero_documento, "000000123")
        self.assertEqual(edoc.prefixo_chave, "NFe" + self.CHAVES_ALFA["55"])

    def test_cfe_alfa_campos(self):
        edoc = ChaveCFeSAT(chave=self.CHAVES_ALFA["59"], validar=True)
        self.assertEqual(edoc.cnpj_cpf_emitente, self.CNPJ_ALFA)
        self.assertEqual(edoc.numero_serie, "900004019")
        self.assertEqual(edoc.codigo_aleatorio, "123456")

    def test_gerar_chave_alfa(self):
        geradas = {
            "55": ("35", "2607", self.CNPJ_ALFA, "001", "000000123"),
            "57": ("41", "2608", "12IBC34D000140", "001", "000004567"),
            "65": ("43", "2607", "12.abc.345/01de-35", "002", "000000010"),
            "58": ("50", "2609", "12.OBC.34D/0001-81", "000", "000000777"),
        }
        for modelo, (uf, aamm, cnpj, serie, numero) in geradas.items():
            with self.subTest(modelo=modelo):
                edoc = ChaveEdoc(
                    codigo_uf=uf,
                    ano_mes=aamm,
                    cnpj_cpf_emitente=cnpj,
                    modelo_documento=modelo,
                    numero_serie=serie,
                    numero_documento=numero,
                    codigo_aleatorio=self.CHAVES_ALFA[modelo][35:43],
                    validar=True,
                )
                self.assertEqual(edoc.chave, self.CHAVES_ALFA[modelo])

    def test_calculo_codigo_aleatorio_alfa(self):
        for modelo in ("55", "57", "58", "65"):
            chave = self.CHAVES_ALFA[modelo]
            with self.subTest(modelo=modelo):
                edoc = ChaveEdoc(chave=chave)
                self.assertEqual(edoc.calculo_codigo_aleatorio(chave[:35]), chave[35:43])

    def test_chave_alfa_dv_errado(self):
        for modelo, chave in self.CHAVES_ALFA.items():
            dv_errado = str((int(chave[-1]) + 1) % 10)
            with self.subTest(modelo=modelo):
                with self.assertRaises(ValueError):
                    detectar_chave_edoc(chave[:43] + dv_errado)

    def test_chave_alfa_letra_fora_do_cnpj(self):
        chave = self.CHAVES_ALFA["55"]
        # cUF, AAMM, DV do CNPJ, modelo, serie, numero, forma, codigo
        posicoes = [0, 3, 5, 18, 19, 20, 23, 30, 34, 36, 42]
        for posicao in posicoes:
            invalida = self._troca(chave, posicao, "A")
            with self.subTest(posicao=posicao):
                with self.assertRaises(ValueError):
                    detectar_chave_edoc(invalida)
                with self.assertRaises(ValueError):
                    ChaveEdoc(chave=invalida)

    def test_chave_alfa_letra_no_dv_da_chave(self):
        chave = self.CHAVES_ALFA["55"]
        with self.assertRaises(ValueError):
            ChaveEdoc(chave=chave[:43] + "A")

    def test_chave_alfa_minuscula(self):
        chave = self.CHAVES_ALFA["55"].replace("ABC", "abc")
        with self.assertRaises(ValueError):
            ChaveEdoc(chave=chave)

    def test_chave_alfa_cnpj_dv_invalido(self):
        # troca uma letra do CNPJ (o DV do CNPJ deixa de bater) e recalcula
        # o DV da chave: a recusa vem da validacao do CNPJ emitente
        invalida = self._troca(self.CHAVES_ALFA["55"], 8, "B")
        with self.assertRaises(ValueError):
            detectar_chave_edoc(invalida)

    def test_gerar_chave_letra_fora_do_cnpj(self):
        with self.assertRaises(ValueError):
            ChaveEdoc(
                codigo_uf="35",
                ano_mes="2607",
                cnpj_cpf_emitente=self.CNPJ_ALFA,
                modelo_documento="55",
                numero_serie="00A",
                numero_documento="000000123",
            )


class TestModulo11(TestCase):
    CHAVES_NUMERICAS = [
        "50131248740351011795580001490001531345952745",
        "43140201098983010680657960000005991148127446",
        "35210320695448000184550010000035891981839923",
        "32171232438772000104570010001990751153183825",
        "35150808723218000186599000040190000241114257",
        "35150808723218000186599000040190000557255950",
        "42221200050690671849559100000000811540256167",
        "32171232438772000104670010001990751234429533",
    ]

    def test_modulo11_numerico_inalterado(self):
        for chave in self.CHAVES_NUMERICAS:
            with self.subTest(chave=chave):
                self.assertEqual(modulo11(chave[:43]), int(chave[-1]))

    def test_modulo11_alfa(self):
        for chave in TestChaveCNPJAlfanumerico.CHAVES_ALFA.values():
            with self.subTest(chave=chave):
                self.assertEqual(modulo11(chave[:43]), int(chave[-1]))

    def test_modulo11_caractere_invalido(self):
        for base in ("12a4", "12 4", "12-4", "12é4"):
            with self.subTest(base=base):
                with self.assertRaises(ValueError):
                    modulo11(base)
