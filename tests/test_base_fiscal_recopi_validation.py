# coding=utf-8
# Copyright (C) 2023  Daniel Venancio - KMEE
# License MIT - See https://opensource.org/license/mit
from unittest import TestCase
from erpbrasil.base.fiscal import recopi


class RecopiValidation(TestCase):
    def setUp(self):
        self.valid_recopi = recopi.generate_valid_recopi()
        self.invalid_recopi_date = '20220229114609734393'
        self.invalid_recopi_no_calendar = '20250229114609734393'
        self.invalid_recopi_time = '20240229274609734393'
        self.invalid_recopi_verification_digit1 = '20231106114609734372'
        self.invalid_recopi_verification_digit2 = '20231106114609734343'
        
    def test_validate_recopi(self):
        test_result = recopi.is_valid_recopi(self.valid_recopi)
        self.assertEqual(True,test_result)

    def test_validate_recopi_date(self):
        test_result = recopi.is_valid_recopi(self.invalid_recopi_date)
        self.assertEqual(False,test_result)

        test_result = recopi.is_valid_recopi(self.invalid_recopi_no_calendar)
        self.assertEqual(False,test_result)
    
    def test_validate_recopi_time(self):
        test_result = recopi.is_valid_recopi(self.invalid_recopi_time)
        self.assertEqual(False,test_result)
    
    def test_validate_recopi_verification_digits(self):
        test_result = recopi.is_valid_recopi(self.invalid_recopi_verification_digit1)
        self.assertEqual(False,test_result)

        test_result = recopi.is_valid_recopi(self.invalid_recopi_verification_digit2)
        self.assertEqual(False,test_result)
