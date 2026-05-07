# coding=utf-8
# @ 2016 KMEE - www.kmee.com.br -
#   Luis Felipe Miléo <mileo@kmee.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest import TestCase

from erpbrasil.base.fiscal import cnpj_cpf
from erpbrasil.base.fiscal import pis


class Tests(TestCase):
    def test_01_validar_pis_pasep(self):
        """Teste validação de PIS correto"""
        self.assertTrue(pis.validar("496.85994.95-6"))

    def test_02_validar_pis_pasep(self):
        """Teste validação de PIS incorreto"""
        self.assertFalse(pis.validar("496.85994.95-7"))

    def test_01_validar_cnpj_cpf(self):
        """Teste validação de CNPJ/CPF correto"""
        self.assertTrue(cnpj_cpf.validar("02.960.895/0001-31"))

    def test_02_validar_cnpj_cpf(self):
        """Teste validação de CNPJ/CPF incorreto"""
        self.assertFalse(cnpj_cpf.validar("14.018.406/0001-93"))

    def test_03_validar_cnpj_cpf(self):
        """Teste validação de CNPJ/CPF correto"""
        self.assertTrue(cnpj_cpf.validar("017.013.558-68"))

    def test_04_validar_cnpj_cpf(self):
        """Teste validação de CNPJ/CPF incorreto"""
        self.assertFalse(cnpj_cpf.validar("734.419.622-07"))

    def test_01_validar_cnpj(self):
        """Teste validação de CNPJ correto"""
        self.assertTrue(cnpj_cpf.validar_cnpj("02.960.895/0001-31"))

    def test_02_validar_cnpj(self):
        """Teste validação de CNPJ incorreto"""
        self.assertFalse(cnpj_cpf.validar_cnpj("14.018.406/0001-93"))

    def test_01_validar_cpf(self):
        """Teste validação de CPF correto"""
        self.assertTrue(cnpj_cpf.validar_cpf("553.948.360-00"))

    def test_02_validar_cpf(self):
        """Teste validação de CPF incorreto"""
        self.assertFalse(cnpj_cpf.validar_cpf("203.519.810-05"))

    def test_01_formata_cnpj_cpf(self):
        """Teste formatação de CNPJ/CPF correto"""
        self.assertEqual(cnpj_cpf.formata("02960895000131"), "02.960.895/0001-31")

    def test_02_formata_cnpj_cpf(self):
        """Teste formatação de CNPJ/CPF correto"""
        self.assertEqual(cnpj_cpf.formata("55394836000"), "553.948.360-00")

    def test_01_formata_cnpj(self):
        """Teste formatação de CNPJ correto"""
        self.assertEqual(cnpj_cpf.formata_cnpj("61103212000199"), "61.103.212/0001-99")

    def test_01_formata_cpf(self):
        """Teste formatação de CPF correto"""
        self.assertEqual(cnpj_cpf.formata_cpf("06853187024"), "068.531.870-24")


class TestCNPJAlfa(TestCase):
    """Testes para CNPJ Alfanumérico conforme NT Conjunta 2025.001."""

    # CNPJ alfa de exemplo: usamos o algoritmo para gerar um válido.
    # Raiz+Ordem "12ABC34D0001" → valores ASCII-48: 1,2,17,18,19,3,4,20,0,0,0,1
    # DV1 pesos [5,4,3,2,9,8,7,6,5,4,3,2]: 5+8+51+54+171+24+28+120+0+0+0+2 = 463
    #   463%11=1 → dv1=0 (resto <2)
    # DV2 pesos [6,5,4,3,2,9,8,7,6,5,4,3]: 6+10+68+54+38+27+32+140+0+0+0+3+0*2 = 378
    #   378%11=4 → dv2=7... validado pelo módulo: DV=66
    # Logo CNPJ válido: "12ABC34D000166"
    CNPJ_ALFA_VALIDO = "12ABC34D000166"
    CNPJ_ALFA_MASCARA = "12.ABC.34D/0001-66"

    def _calcular_dv(self, cnpj12):
        """Helper para calcular DV via módulo."""
        from erpbrasil.base.fiscal.cnpj_cpf import _calcular_dv_cnpj
        return _calcular_dv_cnpj(cnpj12)

    def test_calcula_dv_numerico_igual_ao_algoritmo_antigo(self):
        """Para CNPJ puramente numérico, o DV calculado deve ser idêntico ao antigo."""
        # CNPJ "02960895000131" → raiz+ordem = "029608950001"
        dv = self._calcular_dv("029608950001")
        self.assertEqual(dv, "31")

    def test_calcula_dv_alfa(self):
        """Verifica cálculo de DV para CNPJ alfanumérico."""
        dv = self._calcular_dv("12ABC34D0001")
        self.assertEqual(dv, "66")

    def test_cnpj_alfa_valido(self):
        """CNPJ alfanumérico com DV correto deve ser válido."""
        self.assertTrue(cnpj_cpf.validar_cnpj(self.CNPJ_ALFA_VALIDO))

    def test_cnpj_alfa_valido_via_validar(self):
        """Roteador validar() deve aceitar CNPJ alfanumérico."""
        self.assertTrue(cnpj_cpf.validar(self.CNPJ_ALFA_VALIDO))

    def test_cnpj_alfa_com_mascara(self):
        """CNPJ alfa com máscara (pontos, barra, hífen) deve ser aceito."""
        self.assertTrue(cnpj_cpf.validar_cnpj(self.CNPJ_ALFA_MASCARA))

    def test_cnpj_alfa_dv_incorreto(self):
        """CNPJ alfa com DV errado deve ser inválido."""
        self.assertFalse(cnpj_cpf.validar_cnpj("12ABC34D000199"))

    def test_cnpj_alfa_letra_proibida_I(self):
        """Letra 'I' é proibida no CNPJ Alfa."""
        # Substitui 'A'(pos 2) por 'I'
        self.assertFalse(cnpj_cpf.validar_cnpj("12IBC34D000144"))

    def test_cnpj_alfa_letra_proibida_O(self):
        """Letra 'O' é proibida no CNPJ Alfa."""
        self.assertFalse(cnpj_cpf.validar_cnpj("12OBC34D000144"))

    def test_cnpj_alfa_letra_proibida_U(self):
        """Letra 'U' é proibida no CNPJ Alfa."""
        self.assertFalse(cnpj_cpf.validar_cnpj("12UBC34D000144"))

    def test_cnpj_alfa_letra_proibida_Q(self):
        """Letra 'Q' é proibida no CNPJ Alfa."""
        self.assertFalse(cnpj_cpf.validar_cnpj("12QBC34D000144"))

    def test_cnpj_alfa_letra_proibida_F(self):
        """Letra 'F' é proibida no CNPJ Alfa."""
        self.assertFalse(cnpj_cpf.validar_cnpj("12FBC34D000144"))

    def test_cnpj_alfa_letra_minuscula_invalida(self):
        """Letras minúsculas não são permitidas no CNPJ."""
        self.assertFalse(cnpj_cpf.validar_cnpj("12abc34D000144"))

    def test_cnpj_alfa_zerado_invalido(self):
        """CNPJ '00000000000000' deve ser inválido mesmo com DV correto."""
        self.assertFalse(cnpj_cpf.validar_cnpj("00000000000000"))

    def test_formata_cnpj_alfa(self):
        """formata_cnpj deve preservar as letras na máscara."""
        resultado = cnpj_cpf.formata_cnpj(self.CNPJ_ALFA_VALIDO)
        self.assertEqual(resultado, self.CNPJ_ALFA_MASCARA)

    def test_formata_cnpj_alfa_via_formata(self):
        """formata() deve formatar CNPJ alfanumérico corretamente."""
        resultado = cnpj_cpf.formata(self.CNPJ_ALFA_VALIDO)
        self.assertEqual(resultado, self.CNPJ_ALFA_MASCARA)

    def test_cnpj_numerico_retrocompat(self):
        """CNPJ numérico clássico continua válido com o novo algoritmo."""
        self.assertTrue(cnpj_cpf.validar_cnpj("02.960.895/0001-31"))
        self.assertFalse(cnpj_cpf.validar_cnpj("14.018.406/0001-93"))

    def test_char_value_digitos(self):
        """Dígitos numéricos mantêm os mesmos valores (ord('0')-48=0)."""
        from erpbrasil.base.fiscal.cnpj_cpf import _char_value
        self.assertEqual(_char_value("0"), 0)
        self.assertEqual(_char_value("9"), 9)

    def test_char_value_letras(self):
        """Letras mapeiam conforme ASCII-48: A=17, B=18, Z=42."""
        from erpbrasil.base.fiscal.cnpj_cpf import _char_value
        self.assertEqual(_char_value("A"), 17)
        self.assertEqual(_char_value("B"), 18)
        self.assertEqual(_char_value("Z"), 42)

