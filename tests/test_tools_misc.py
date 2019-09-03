# coding=utf-8
# @ 2019 Akretion - www.akretion.com.br -
#   Magno Costa <magno.costa@akretion.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest import TestCase

from erpbrasil.base.misc import calc_price_ratio
from erpbrasil.base.misc import punctuation_rm


class Tests(TestCase):

    def test_punctution_rm(self):
        self.assertEqual(
            punctuation_rm('496.85994.95-7'), '49685994957',
            'The function punctuation_rm failed.')

    def test_calc_price_ratio(self):
        self.assertEqual(
            calc_price_ratio(10, 100, 1000), 1.0,
            'The function calc_price_ratio failed.')
        self.assertEqual(
            calc_price_ratio(10, 100, 0), 0,
            'The function calc_price_ratio failed.')
