# Copyright (C) 2024 Renato Lima
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

"""Testes para o módulo dfe.py (ChaveDFe e ChaveCFeSAT).

Cobre:
- Imports diretos do novo módulo dfe
- Propriedades com nomenclatura oficial XML (cUF, dhEmi, mod, serie, nNF,
  tpEmis, nSiteAutoriz, cNF, cDV, dfe_key)
- Geração de chave a partir de campos individuais com nomes oficiais
- Retrocompatibilidade das propriedades legadas via ChaveDFe
"""

from unittest import TestCase

from erpbrasil.base.fiscal.dfe import ChaveCFeSAT
from erpbrasil.base.fiscal.dfe import ChaveDFe
from erpbrasil.base.fiscal.dfe import detectar_chave_dfe


class TestChaveDFePropriedadesOficiais(TestCase):
    """Testa as propriedades com nomenclatura oficial do schema XML."""

    def setUp(self):
        # NF-e conhecida, usada em vários testes
        self.chave_nfe = "35210320695448000184550010000035891981839923"
        self.dfe = ChaveDFe(chave=self.chave_nfe)

    def test_dfe_key(self):
        """dfe_key deve retornar a chave completa de 44 dígitos."""
        self.assertEqual(self.dfe.dfe_key, self.chave_nfe)
        self.assertEqual(len(self.dfe.dfe_key), 44)

    def test_cUF(self):
        """cUF deve retornar o código IBGE da UF como inteiro."""
        self.assertEqual(self.dfe.cUF, 35)  # SP

    def test_dhEmi(self):
        """dhEmi deve retornar o ano/mês no formato AAMM."""
        self.assertEqual(self.dfe.dhEmi, "2103")

    def test_mod(self):
        """mod deve retornar o modelo do documento (2 dígitos)."""
        self.assertEqual(self.dfe.mod, "55")

    def test_serie(self):
        """serie deve retornar a série do documento (3 dígitos)."""
        self.assertEqual(self.dfe.serie, "001")

    def test_nNF(self):
        """nNF deve retornar o número do documento (9 dígitos)."""
        self.assertEqual(self.dfe.nNF, "000003589")

    def test_tpEmis(self):
        """tpEmis deve retornar a forma de emissão (1 dígito)."""
        self.assertEqual(self.dfe.tpEmis, "1")

    def test_cNF(self):
        """cNF deve retornar o código numérico (8 dígitos para NF-e)."""
        self.assertEqual(self.dfe.cNF, "98183992")
        self.assertEqual(len(self.dfe.cNF), 8)

    def test_cDV(self):
        """cDV deve retornar o dígito verificador (1 dígito)."""
        self.assertEqual(self.dfe.cDV, "3")

    def test_nSiteAutoriz_nao_aplicavel(self):
        """nSiteAutoriz deve ser False para NF-e (modelo sem site autoriz)."""
        self.assertFalse(self.dfe.nSiteAutoriz)


class TestChaveDFePropriedadesLegadas(TestCase):
    """Garante retrocompatibilidade das propriedades legadas em ChaveDFe."""

    def setUp(self):
        self.chave_nfe = "35210320695448000184550010000035891981839923"
        self.dfe = ChaveDFe(chave=self.chave_nfe)

    def test_codigo_uf_alias(self):
        self.assertEqual(self.dfe.codigo_uf, self.dfe.cUF)

    def test_ano_mes_alias(self):
        self.assertEqual(self.dfe.ano_mes, self.dfe.dhEmi)

    def test_modelo_documento_alias(self):
        self.assertEqual(self.dfe.modelo_documento, self.dfe.mod)

    def test_numero_serie_alias(self):
        self.assertEqual(self.dfe.numero_serie, self.dfe.serie)

    def test_numero_documento_alias(self):
        self.assertEqual(self.dfe.numero_documento, self.dfe.nNF)

    def test_forma_emissao_alias(self):
        self.assertEqual(self.dfe.forma_emissao, self.dfe.tpEmis)

    def test_codigo_aleatorio_alias(self):
        self.assertEqual(self.dfe.codigo_aleatorio, self.dfe.cNF)

    def test_digito_verificador_alias(self):
        self.assertEqual(self.dfe.digito_verificador, self.dfe.cDV)

    def test_site_autorizador_alias(self):
        self.assertEqual(self.dfe.site_autorizador, self.dfe.nSiteAutoriz)

    def test_ano_emissao(self):
        self.assertEqual(self.dfe.ano_emissao, 2021)

    def test_mes_emissao(self):
        self.assertEqual(self.dfe.mes_emissao, 3)


class TestChaveDFeGeracaoNomesOficiais(TestCase):
    """Testa geração de chave usando os nomes oficiais do schema XML."""

    def test_gera_chave_nfe_nomes_oficiais(self):
        """Deve gerar a mesma chave usando nomes oficiais ou legados."""
        chave_esperada = "35210320695448000184550010000035891981839923"

        dfe_oficial = ChaveDFe(
            cUF=35,
            dhEmi="2103",
            CNPJ="20.695.448/0001-84",
            mod="55",
            serie="001",
            nNF="000003589",
            tpEmis=1,
        )
        self.assertEqual(dfe_oficial.dfe_key, chave_esperada)

    def test_gera_chave_nomes_legados_equivalentes(self):
        """Nomes legados devem produzir a mesma chave que os nomes oficiais."""
        chave_esperada = "35210320695448000184550010000035891981839923"

        dfe_legado = ChaveDFe(
            codigo_uf=35,
            ano_mes="2103",
            cnpj_cpf_emitente="20.695.448/0001-84",
            modelo_documento="55",
            numero_serie="001",
            numero_documento="000003589",
            forma_emissao=1,
        )
        self.assertEqual(dfe_legado.dfe_key, chave_esperada)

    def test_gera_chave_nf3e_com_site_autoriz_nomes_oficiais(self):
        """Deve gerar chave NF3e (mod 66) com nSiteAutoriz usando nomes oficiais."""
        dfe = ChaveDFe(
            cUF=35,
            dhEmi="2401",
            CNPJ="02.960.895/0001-31",
            mod="66",
            serie="001",
            nNF="123456789",
            tpEmis=1,
            nSiteAutoriz="2",
            validar=True,
        )
        self.assertEqual(dfe.mod, "66")
        self.assertEqual(dfe.nSiteAutoriz, "2")
        self.assertEqual(len(dfe.cNF), 7)
        self.assertEqual(len(dfe.dfe_key), 44)

    def test_gera_chave_com_cpf_emitente(self):
        """Deve aceitar CPF como documento do emitente."""
        dfe = ChaveDFe(
            cUF=42,
            dhEmi="2212",
            CPF="00050690671849",  # CPF com zeros à esquerda (14 posições)
            mod="55",
            serie="920",           # faixa CPF
            nNF="000000081",
            tpEmis=1,
        )
        self.assertEqual(len(dfe.dfe_key), 44)
        self.assertEqual(dfe.serie, "920")


class TestChaveDFeValidacao(TestCase):
    """Testa o método validar() em ChaveDFe."""

    def test_valida_nfe(self):
        chave = "35210320695448000184550010000035891981839923"
        dfe = ChaveDFe(chave=chave, validar=True)
        self.assertEqual(dfe.dfe_key, chave)

    def test_valida_cte(self):
        chave = "32171232438772000104570010001990751153183825"
        dfe = ChaveDFe(chave=chave, validar=True)
        self.assertEqual(dfe.mod, "57")

    def test_valida_mdfe(self):
        chave = "50131248740351011795580001490001531345952745"
        dfe = ChaveDFe(chave=chave, validar=True)
        self.assertEqual(dfe.mod, "58")

    def test_rejeita_uf_invalida(self):
        chave = "99150808723218000186599000040190000241114257"
        with self.assertRaises(ValueError):
            ChaveDFe(chave=chave, validar=True)

    def test_rejeita_dv_errado(self):
        # Último dígito alterado de 3 → 4
        chave = "35210320695448000184550010000035891981839924"
        with self.assertRaises(ValueError):
            ChaveDFe(chave=chave, validar=True)

    def test_rejeita_modelo_invalido(self):
        # Modelo 54 não existe
        chave = "35210320695448000184540010000035891981839924"
        with self.assertRaises(ValueError):
            ChaveDFe(chave=chave, validar=True)


class TestDetectarChaveDfe(TestCase):
    """Testa a função detectar_chave_dfe."""

    def test_detecta_nfe(self):
        chave = "35210320695448000184550010000035891981839923"
        dfe = detectar_chave_dfe(chave)
        self.assertIsInstance(dfe, ChaveDFe)
        self.assertEqual(dfe.mod, "55")

    def test_detecta_cfe_sat(self):
        chave = "35150808723218000186599000040190000241114257"
        dfe = detectar_chave_dfe(chave)
        self.assertIsInstance(dfe, ChaveCFeSAT)
        self.assertEqual(dfe.mod, "59")

    def test_rejeita_chave_invalida(self):
        with self.assertRaises(ValueError):
            detectar_chave_dfe("chave_invalida")

    def test_chaves_validas_conhecidas(self):
        chaves = [
            "50131248740351011795580001490001531345952745",
            "43140201098983010680657960000005991148127446",
            "35210320695448000184550010000035891981839923",
            "32171232438772000104570010001990751153183825",
            "42221200050690671849559100000000811540256167",
        ]
        for chave in chaves:
            with self.subTest(chave=chave):
                dfe = detectar_chave_dfe(chave)
                self.assertEqual(len(dfe.dfe_key), 44)


class TestChaveCFeSATNomesOficiais(TestCase):
    """Testa ChaveCFeSAT com os novos nomes de propriedades."""

    def setUp(self):
        self.chave = "35150808723218000186599000040190000557255950"
        self.cfe = ChaveCFeSAT(chave=self.chave)

    def test_dfe_key(self):
        self.assertEqual(self.cfe.dfe_key, self.chave)

    def test_cUF(self):
        self.assertEqual(self.cfe.cUF, 35)

    def test_dhEmi(self):
        self.assertEqual(self.cfe.dhEmi, "1508")

    def test_mod(self):
        self.assertEqual(self.cfe.mod, "59")

    def test_serie_nove_digitos(self):
        """CF-e SAT tem serie de 9 dígitos."""
        self.assertEqual(self.cfe.serie, "900004019")
        self.assertEqual(len(self.cfe.serie), 9)

    def test_nNF_seis_digitos(self):
        """CF-e SAT tem nNF de 6 dígitos."""
        self.assertEqual(self.cfe.nNF, "000055")
        self.assertEqual(len(self.cfe.nNF), 6)

    def test_tpEmis_vazio(self):
        """CF-e SAT não possui tpEmis."""
        self.assertEqual(self.cfe.tpEmis, "")

    def test_cNF_seis_digitos(self):
        """CF-e SAT tem cNF de 6 dígitos."""
        self.assertEqual(self.cfe.cNF, "725595")
        self.assertEqual(len(self.cfe.cNF), 6)

    def test_cDV(self):
        self.assertEqual(self.cfe.cDV, "0")

    def test_nSiteAutoriz_nao_aplicavel(self):
        self.assertFalse(self.cfe.nSiteAutoriz)


class TestRetrocompatibilidadeEdocImports(TestCase):
    """Garante que importar de edoc ainda funciona (stub de compatibilidade)."""

    def test_importa_chave_edoc(self):
        from erpbrasil.base.fiscal.edoc import ChaveEdoc
        chave = "35210320695448000184550010000035891981839923"
        obj = ChaveEdoc(chave=chave)
        # ChaveEdoc é alias de ChaveDFe, deve ter as novas propriedades
        self.assertEqual(obj.dfe_key, chave)
        self.assertEqual(obj.cUF, 35)
        self.assertEqual(obj.mod, "55")

    def test_importa_detectar_chave_edoc(self):
        from erpbrasil.base.fiscal.edoc import detectar_chave_edoc
        chave = "35210320695448000184550010000035891981839923"
        obj = detectar_chave_edoc(chave)
        self.assertEqual(obj.dfe_key, chave)

    def test_importa_chave_cfe_sat(self):
        from erpbrasil.base.fiscal.edoc import ChaveCFeSAT
        chave = "35150808723218000186599000040190000557255950"
        obj = ChaveCFeSAT(chave=chave)
        self.assertEqual(obj.mod, "59")


class TestProcEmi(TestCase):
    """Testa o campo procEmi (processo de emissão, id:B26)."""

    # Chave NF-e válida, série 001 → faixa app do contribuinte (procEmi 0 ou 3)
    CHAVE_NFE = "35210320695448000184550010000035891981839923"
    # Chave NF-e válida com CPF, série 920 → faixa CPF app contribuinte (procEmi 0)
    CHAVE_NFE_CPF = "42221200050690671849559100000000811540256167"

    def test_proc_emi_none_por_padrao(self):
        """Sem procEmi informado, propriedade deve retornar None."""
        dfe = ChaveDFe(chave=self.CHAVE_NFE)
        self.assertIsNone(dfe.procEmi)

    def test_proc_emi_armazenado(self):
        """procEmi informado deve ser acessível pela propriedade."""
        dfe = ChaveDFe(chave=self.CHAVE_NFE, procEmi=0)
        self.assertEqual(dfe.procEmi, 0)

    def test_proc_emi_descricao(self):
        """procEmi_descricao deve retornar a string descritiva correta."""
        dfe = ChaveDFe(chave=self.CHAVE_NFE, procEmi=0)
        self.assertIn("aplicativo do contribuinte", dfe.procEmi_descricao)

        dfe2 = ChaveDFe(chave=self.CHAVE_NFE, procEmi=1)
        self.assertIn("avulsa pelo Fisco", dfe2.procEmi_descricao)

        dfe3 = ChaveDFe(chave=self.CHAVE_NFE, procEmi=3)
        self.assertIn("fornecido pelo Fisco", dfe3.procEmi_descricao)

    def test_proc_emi_descricao_none_sem_valor(self):
        """procEmi_descricao deve ser None quando procEmi não foi informado."""
        dfe = ChaveDFe(chave=self.CHAVE_NFE)
        self.assertIsNone(dfe.procEmi_descricao)

    def test_proc_emi_valido_com_serie_correta(self):
        """procEmi=0 com série 001 (faixa 000-889) deve passar a validação."""
        dfe = ChaveDFe(chave=self.CHAVE_NFE, procEmi=0, validar=True)
        self.assertEqual(dfe.procEmi, 0)

    def test_proc_emi_3_com_serie_correta(self):
        """procEmi=3 com série 001 (faixa 000-889) deve passar a validação."""
        dfe = ChaveDFe(chave=self.CHAVE_NFE, procEmi=3, validar=True)
        self.assertEqual(dfe.procEmi, 3)

    def test_proc_emi_serie_incompativel_rejeicao_266(self):
        """procEmi=1 com série 001 (fora da faixa 890-899) deve falhar (Rejeição 266)."""
        with self.assertRaises(ValueError) as ctx:
            ChaveDFe(chave=self.CHAVE_NFE, procEmi=1, validar=True)
        self.assertIn("266", str(ctx.exception))

    def test_proc_emi_2_serie_incompativel_rejeicao_266(self):
        """procEmi=2 com série 001 (fora da faixa 900-919) deve falhar (Rejeição 266)."""
        with self.assertRaises(ValueError) as ctx:
            ChaveDFe(chave=self.CHAVE_NFE, procEmi=2, validar=True)
        self.assertIn("266", str(ctx.exception))

    def test_proc_emi_invalido(self):
        """Valor de procEmi fora de {0,1,2,3} deve levantar ValueError."""
        with self.assertRaises(ValueError):
            ChaveDFe(chave=self.CHAVE_NFE, procEmi=9, validar=True)

    def test_proc_emi_nao_valida_sem_flag_validar(self):
        """Sem validar=True, procEmi incompatível não deve levantar exceção."""
        # Não deve lançar exceção mesmo com combinação inválida
        dfe = ChaveDFe(chave=self.CHAVE_NFE, procEmi=1)
        self.assertEqual(dfe.procEmi, 1)

    def test_proc_emi_ignorado_para_cte(self):
        """procEmi não valida série para documentos que não sejam NF-e/NFC-e."""
        chave_cte = "32171232438772000104570010001990751153183825"
        # procEmi=1 com série 001 em CT-e não deve rejeitar
        dfe = ChaveDFe(chave=chave_cte, procEmi=1, validar=True)
        self.assertEqual(dfe.mod, "57")
        self.assertEqual(dfe.procEmi, 1)

    def test_proc_emi_importado_de_constantes(self):
        """PROC_EMI e PROC_EMI_SERIES devem estar disponíveis no módulo."""
        from erpbrasil.base.fiscal.dfe import PROC_EMI, PROC_EMI_SERIES
        self.assertIn(0, PROC_EMI)
        self.assertIn(1, PROC_EMI)
        self.assertIn(2, PROC_EMI)
        self.assertIn(3, PROC_EMI)
        self.assertIn(0, PROC_EMI_SERIES)
        # Série 001 deve estar em procEmi=0
        self.assertIn(1, PROC_EMI_SERIES[0])
        # Série 895 deve estar em procEmi=1
        self.assertIn(895, PROC_EMI_SERIES[1])
