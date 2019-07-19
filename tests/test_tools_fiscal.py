# coding=utf-8
# @ 2016 KMEE - www.kmee.com.br -
#   Luis Felipe Miléo <mileo@kmee.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest import TestCase

from erpbrasil.base.fiscal import validate_cnpj
from erpbrasil.base.fiscal import validate_cpf
from erpbrasil.base.fiscal import validate_pis_pasep


class Tests(TestCase):

    def test_01_validate_pis_pasep(self):
        self.assertTrue(validate_pis_pasep('496.85994.95-6'))

    def test_02_validate_pis_pasep(self):
        self.assertFalse(validate_pis_pasep('496.85994.95-7'))

    def test_01_validate_cnpj(self):
        self.assertTrue(validate_cnpj('02.960.895/0001-31'))

    def test_02_validate_cnpj(self):
        self.assertFalse(validate_cnpj('14.018.406/0001-93'))

    def test_01_validate_cpf(self):
        self.assertTrue(validate_cpf('017.013.558-68'))

    def test_02_validate_cpf(self):
        self.assertFalse(validate_cpf('734.419.622-07'))
