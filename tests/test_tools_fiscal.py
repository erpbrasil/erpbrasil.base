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
        self.assertTrue(pis.validar('496.85994.95-6'))

    def test_02_validar_pis_pasep(self):
        """Teste validação de PIS incorreto"""
        self.assertFalse(pis.validar('496.85994.95-7'))

    def test_01_validar_cnpj_cpf(self):
        """Teste validação de CNPJ/CPF correto"""
        self.assertTrue(cnpj_cpf.validar('02.960.895/0001-31'))

    def test_02_validar_cnpj_cpf(self):
        """Teste validação de CNPJ/CPF incorreto"""
        self.assertFalse(cnpj_cpf.validar('14.018.406/0001-93'))

    def test_03_validar_cnpj_cpf(self):
        """Teste validação de CNPJ/CPF correto"""
        self.assertTrue(cnpj_cpf.validar('017.013.558-68'))

    def test_04_validar_cnpj_cpf(self):
        """Teste validação de CNPJ/CPF incorreto"""
        self.assertFalse(cnpj_cpf.validar('734.419.622-07'))

    def test_01_validar_cnpj(self):
        """Teste validação de CNPJ correto"""
        self.assertTrue(cnpj_cpf.validar_cnpj('02.960.895/0001-31'))

    def test_02_validar_cnpj(self):
        """Teste validação de CNPJ incorreto"""
        self.assertFalse(cnpj_cpf.validar_cnpj('14.018.406/0001-93'))

    def test_01_validar_cpf(self):
        """Teste validação de CPF correto"""
        self.assertTrue(cnpj_cpf.validar_cpf('553.948.360-00'))

    def test_02_validar_cpf(self):
        """Teste validação de CPF incorreto"""
        self.assertFalse(cnpj_cpf.validar_cpf('203.519.810-05'))

    def test_01_formata_cnpj_cpf(self):
        """Teste formatação de CNPJ/CPF correto"""
        self.assertEqual(
            cnpj_cpf.formata('02960895000131'), '02.960.895/0001-31')

    def test_02_formata_cnpj_cpf(self):
        """Teste formatação de CNPJ/CPF correto"""
        self.assertEqual(
            cnpj_cpf.formata('55394836000'), '553.948.360-00')

    def test_01_formata_cnpj(self):
        """Teste formatação de CNPJ correto"""
        self.assertEqual(
            cnpj_cpf.formata_cnpj('61103212000199'), '61.103.212/0001-99')

    def test_01_formata_cpf(self):
        """Teste formatação de CPF correto"""
        self.assertEqual(
            cnpj_cpf.formata_cpf('06853187024'), '068.531.870-24')
