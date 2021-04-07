# coding=utf-8
# @ 2019 Akretion - www.akretion.com.br -
#   Magno Costa <magno.costa@akretion.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest import TestCase

from erpbrasil.base.misc import calc_price_ratio
from erpbrasil.base.misc import format_zipcode
from erpbrasil.base.misc import modulo11
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

    def test_format_zipcode(self):
        self.assertEqual(
            format_zipcode('12327130'), '12327-130',
            'The function format_zipcode failed.')

    def test_modulo_11(self):
        self.assertEqual(
            modulo11('0'), 0, 'The function modulo11 failed.'
        )
        self.assertEqual(
            modulo11('6'), 0, 'The function modulo11 failed.'
        )
        self.assertEqual(
            modulo11('1'), 9, 'The function modulo11 failed.'
        )

        # MDFe50131248740351011795580001490001531345952745
        # NFe43140201098983010680657960000005991148127446
        # CFe35150808723218000186599000040190000241114257

        self.assertEqual(
            modulo11('5013124874035101179558000149000153134595274'), 5,
            'The function modulo11 failed.'
        )
        self.assertEqual(
            modulo11('4314020109898301068065796000000599114812744'), 6,
            'The function modulo11 failed.'
        )
        self.assertEqual(
            modulo11('3515080872321800018659900004019000024111425'), 7,
            'The function modulo11 failed.'
        )
