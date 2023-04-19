# Copyright (C) 2023  Tiago Amaral - KMEE
# License MIT - See https://opensource.org/license/mit/


from unittest import TestCase

from erpbrasil.base.fiscal import bacen

INVALIDOS = [
    "2",
    "3",
    "4",
    "5",
    "0A12",
    "1",
    "00001",
    "1504",
    "1508",
    "4525",
    "3595",
    "4985",
    "6781",
    "7370",
]
VALIDOS = ["1058", "5860", "0698", "1155", "0310"]


class Tests(TestCase):
    """Testando os casos válidos e inválidos"""

    def test_01_invalidar_bacen_invalidos(self):
        """Invalidando BACEN inválidos"""
        for bacen_invalido in INVALIDOS:
            self.assertFalse(bacen.validar(bacen_invalido))

    def test_02_validar_bacen_validos(self):
        """Validando BACEN válidos"""
        for bacen_valido in VALIDOS:
            self.assertTrue(bacen.validar(bacen_valido))
