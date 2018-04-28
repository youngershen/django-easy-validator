# PROJECT : validator
# TIME : 17-9-16 上午10:14
# AUTHOR : Younger Shen
# EMAIL : younger.x.shen@gmail.com
from django.test import TestCase
from .validators import Validator


class Required(Validator):
    username = 'required'

    message = {
        'username': {
            'required': 'username is required'
        }
    }


class Accepted(Validator):
    remember = 'accepted'

    message = {
        'remember': {
            'accepted': 'input of {VALUE} is not accepted in {FLAGS}'
        }
    }


class AcceptedCustom(Validator):
    remember = 'accepted'
    flag = ['shi', 'fou']

    message = {
        'remember': {
            'accepted': ''
        }
    }


class RequiredTestCase(TestCase):
    def setUp(self):
        self.validator = Required

        self.valid_data = {
            'username': 'batman'
        }

        self.invalid_data = {
            'username': ''
        }

        self.message = {
            'username': {
                'required': 'username is required'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())
        message = validator.get_message()
        self.assertDictEqual(message, self.message)


class AcceptedTestCase(TestCase):
    def setUp(self):
        self.validator = Accepted
        self.valid_data = {
            'remember': 'yes'
        }
        self.invalid_data = {
            'remember': 'none'
        }

        self.message = {
            'remember': {
                'accepted': 'input of none is not accepted in yes, no, true, false, 0, 1'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())
        message = validator.get_message()
        self.assertDictEqual(message, self.message)
