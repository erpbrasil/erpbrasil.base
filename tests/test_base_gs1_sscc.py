# coding=utf-8
# Copyright (C) 2022  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from unittest import TestCase

from erpbrasil.base.gs1 import sscc, gtin

VALID_SSCC = [
    "280606423387880180", "956875422681722846", "059151604654252344",
    "726522690941446201", "923729969874708453", "315675935632281424",
    "981753756950843057", "421461035827133389", "114501260103326034",
    "977482279054687535", "242814236499531971", "101941732188141054",
    "336297483901904679", "166594915478725195", "692711179288758968",
    "574859683190970625", "287707447691589574", "854564014561187607",
    "113649860440240288", "800780031006479502",
]

INVALID_SSCC = [
    "305788967459080265", "758770305603728414", "883581652244784805",
    "978008100983174208", "154184175133162437", "171910190499565073",
    "283691452069313742", "265389226294799584", "133140809139037012",
    "044342926527020754", "678890503918969616", "651509666443879115",
    "342504535786675752", "134185959932399354", "884202258801632486",
    "767077540261141177", "326901160728668955", "728372849963190027",
    "178232290913187517", "150563553863363335",
]

class Tests(TestCase):

    def test_sscc_valid(self):
        """Teste para validação de SSCC válidos"""

        for sscc_number in VALID_SSCC:
            self.assertTrue(
                sscc.validar(sscc_number),
                'Error on validate valid %s SSCC' % sscc_number
            )

    def test_sscc_invalid(self):
        """Teste para validação de SSCC inválidos"""

        for sscc_number in INVALID_SSCC:
            self.assertFalse(
                sscc.validar(sscc_number),
                'Error on validate invalid %s SSCC' % sscc_number
            )

    def test_sscc_invalid_length(self):
        """Teste para validação de SSCC com tamanhos inválidos"""

        sscc_numbers = ["1782322908699967517345253", "178324232"]

        for sscc_number in sscc_numbers:
            self.assertFalse(
                sscc.validar(sscc_number),
                'Error on validate invalid length %s SSCC' % sscc_number
            )

    def test_gerar_sscc(self):
        """Teste para geração de SSCC válidos"""

        sscc_codes = gtin.gerar_gs1_code(18, 20)

        self.assertEqual(
            len(sscc_codes), 20, 'The function gerar in SSCC failed.')

        for sscc_number in sscc_codes:
            self.assertTrue(
                sscc.validar(sscc_number),
                'Error on validate valid %s SSCC' % sscc_number
            )
