# Copyright (C) 2023  Breno Dias - KMEE
# License MIT - See https://opensource.org/license/mit

from erpbrasil.base.fiscal import suframa

from unittest import TestCase
# Create a list with invalid suframa codes
invalid_suframa = ['1234567', '1234567890', '123456788', '423456780', '008451788']

# Create a list with valid suframa codes
valid_suframa = ['123456789', '143456784', '148456782', '148451780', '088451780']


class ValidateSuframaTest(TestCase):

    def test_suframa_invalid(self):
        for cod in invalid_suframa:
            self.assertFalse(
                suframa.validar(cod),
                'Error on validate %s suframa' % cod
            )

    def test_suframa_valid(self):
        for cod in valid_suframa:
            self.assertTrue(
                suframa.validar(cod),
                'Error on validate %s suframa' % cod
            )

