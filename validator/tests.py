# PROJECT : validator
# TIME : 17-9-16 上午10:14
# AUTHOR : Younger Shen
# EMAIL : younger.x.shen@gmail.com
from django.test import TestCase
from validator import Validator


class TestValidator(Validator):
    test = 'required'

    message = {

    }

    info = {
        0: '',
        1: '',
        2: ''
    }

    def check(self):
        pass


class Got(TestCase):

    @staticmethod
    def test_fuck():
        assert True

    @staticmethod
    def test_ssss():
        a = TestValidator({}, '')
        a.validate()
        print(a.get_message())
        assert True
