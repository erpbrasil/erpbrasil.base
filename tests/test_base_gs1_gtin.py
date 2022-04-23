# coding=utf-8
# Copyright (C) 2022  Renato Lima - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from unittest import TestCase

from erpbrasil.base.gs1 import gtin

VALID_GTIN = [
    "00074887615305", "00076950450233", "00011194365349", "00025700395720",
    "09780262134729", "00764014835521", "00839728000388", "00072180634733",
    "00051000121141", "00024300735738", "00078000003154", "00839451002055",
    "00038000845000", "00038000844966", "00041500805054", "00078742370873",
    "00085239147238", "00052100006987", "00605388187239", "00021131509071",
    "00072319005915", "00031200016058", "00038000317200", "00041800207503",
    "00016000503304", "00041500000312", "00048500019047", "0008346045716",
    "00099482441159", "00081308001425", "00031000307448", "00738435265120",
    "00021130035236", "09781591844099", "09780307465351", "00644209412808",
]

INVALID_GTIN = [
    "09781585421464", "09780984999305", "09780312425072", "00381370044317",
    "00883484708909", "00017000046493", "00077043104506", "00037000062211",
    "00035000896504", "00011509211327", "00072140813524", "00041167066237",
    "00019045105394", "00049022428558", "00021428951451", "00000000915905",
    "00017000026707", "00011110881783", "00692991701920", "00043000950653",
    "00037000201781", "00610290249453", "00013051323827", "00084114032404",
    "00073950278193", "00016000275647", "000160", "000160000034342434234",
]

class Tests(TestCase):

    def test_gtin_valid(self):
        """Teste para validação de GTIN válidos"""
        for gtin_number in VALID_GTIN:
            self.assertTrue(
                gtin.validar(gtin_number),
                'Error on validate valid %s GTIN' % gtin_number
            )

    def test_gtin_invalid(self):
        """Teste para validação de GTIN inválidos"""
        for gtin_number in INVALID_GTIN:
            self.assertFalse(
                gtin.validar(gtin_number),
                'Error on validate invalid %s GTIN' % gtin_number
            )

    def test_gtin_invalid_length(self):
        """Teste para validação de GTIN com tamanhos inválidos"""

        gtin_numbers = ["178232290913187517345253", "178232"]

        for gtin_number in gtin_numbers:
            self.assertFalse(
                gtin.validar(gtin_number),
                'Error on validate invalid length %s GTIN' % gtin_number
            )

    def test_gerar_gtin_8(self):
        """Teste para geração de GTIN-8 válidos"""

        gtin_codes = gtin.gerar_gs1_code(8, 20)

        self.assertEqual(
            len(gtin_codes), 20, 'The function gerar in GTIN-8 failed.')

        for gtin_number in gtin_codes:
            self.assertTrue(
                gtin.validar(gtin_number),
                'Error on validate valid %s GTIN-8' % gtin_number
            )

    def test_gerar_gtin_12(self):
        """Teste para geração de GTIN-12 válidos"""

        gtin_codes = gtin.gerar_gs1_code(12, 20)

        self.assertEqual(
            len(gtin_codes), 20, 'The function gerar in GTIN-12 failed.')

        for gtin_number in gtin_codes:
            self.assertTrue(
                gtin.validar(gtin_number),
                'Error on validate valid %s GTIN-12' % gtin_number
            )

    def test_gerar_gtin_13(self):
        """Teste para geração de GTIN-13 válidos"""

        gtin_codes = gtin.gerar_gs1_code(13, 20)

        self.assertEqual(
            len(gtin_codes), 20, 'The function gerar in GTIN-13 failed.')

        for gtin_number in gtin_codes:
            self.assertTrue(
                gtin.validar(gtin_number),
                'Error on validate valid %s GTIN-13' % gtin_number
            )

    def test_gerar_gtin_14(self):
        """Teste para geração de GTIN-14 válidos"""

        gtin_codes = gtin.gerar_gs1_code(14, 20)

        self.assertEqual(
            len(gtin_codes), 20, 'The function gerar in GTIN-14 failed.')

        for gtin_number in gtin_codes:
            self.assertTrue(
                gtin.validar(gtin_number),
                'Error on validate valid %s GTIN-14' % gtin_number
            )
