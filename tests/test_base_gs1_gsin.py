# coding=utf-8
# Copyright (C) 2022  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from unittest import TestCase

from erpbrasil.base.gs1 import gsin
from erpbrasil.base.gs1 import gtin

VALID_GSIN = [
    "71192721913505061",
    "75063182415800547",
    "28017720294220567",
    "62245947641758602",
    "18830266445851111",
    "54488055694458115",
    "89129510271659702",
    "27391931274270492",
    "65860345475528332",
    "04169036102499350",
    "24872490975559187",
    "84683188442872793",
    "89919061076384603",
    "48532538903592972",
    "46840683235076620",
    "62048406522930647",
    "67630373178921285",
    "52578137069169456",
    "11883617783405680",
    "69181438619392246",
]

INVALID_GSIN = [
    "18772726726689673",
    "16595492275373822",
    "01600357275522628",
    "55777838555840572",
    "07379514186898403",
    "46164158961350892",
    "96089636911102291",
    "12760947494490816",
    "60107845852650329",
    "55386076645767996",
    "44675491969796748",
    "71341478737121171",
    "02689337868320117",
    "86496235335507052",
    "72562845886994815",
    "17074532382374823",
    "31136708950510517",
    "45415819674654564",
    "51789934787762035",
    "37983028770565954",
]


class Tests(TestCase):
    def test_gsin_valid(self):
        """Teste para validação de GSIN válidos"""

        for gsin_number in VALID_GSIN:
            self.assertTrue(
                gsin.validar(gsin_number),
                "Error on validate valid %s GSIN" % gsin_number,
            )

    def test_gsin_invalid(self):
        """Teste para validação de GSIN inválidos"""

        for gsin_number in INVALID_GSIN:
            self.assertFalse(
                gsin.validar(gsin_number),
                "Error on validate invalid %s GSIN" % gsin_number,
            )

    def test_gsin_invalid_length(self):
        """Teste para validação de GSIN com tamanhos inválidos"""

        gsin_numbers = ["1782322908699967517345253", "178324232"]

        for gsin_number in gsin_numbers:
            self.assertFalse(
                gsin.validar(gsin_number),
                "Error on validate invalid length %s GSIN" % gsin_number,
            )

    def test_gerar_gsin(self):
        """Teste para geração de GSIN válidos"""

        gsin_codes = gtin.gerar_gs1_code(17, 20)

        self.assertEqual(len(gsin_codes), 20, "The function gerar in gsin failed.")

        for gsin_number in gsin_codes:
            self.assertTrue(
                gsin.validar(gsin_number),
                "Error on validate valid %s GSIN" % gsin_number,
            )
