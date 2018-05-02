# PROJECT : validator
# TIME : 17-9-16 上午10:14
# AUTHOR : Younger Shen
# EMAIL : younger.x.shen@gmail.com
from django.test import TestCase
from validator import Validator


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
    remember = 'accepted:shi,fou'
    message = {
        'remember': {
            'accepted': 'you just input {VALUE}'
        }
    }


class Date(Validator):
    birthday = 'date'
    message = {
        'birthday': {
            'date': 'date format is invalid'
        }
    }


class DateCustom(Validator):
    birthday = 'date:%Y'
    message = {
        'birthday': {
            'date': 'date format is not ok'
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


class AcceptedCustomTestCase(TestCase):
    def setUp(self):
        self.validator = AcceptedCustom
        self.valid_data = {
            'remember': 'shi'
        }

        self.invalid_data = {
            'remember': 'bushi'
        }

        self.message = {
            'remember': {
                'accepted': 'you just input bushi'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())
        self.assertDictEqual(validator.get_message(), self.message)


class DateTestCase(TestCase):
    def setUp(self):
        self.validator = Date
        self.valid_data = {
            'birthday': '1990-12-12'
        }
        self.invalid_data = {
            'birthday': 'not a date'
        }

        self.message = {
            'birthday': {
                'date': 'date format is invalid'
            }
        }

    def test_vald(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())
        self.assertDictEqual(validator.get_message(), self.message)


class DateCustomTestCase(TestCase):
    def setUp(self):
        self.validator = DateCustom
        self.valid_data = {
            'birthday': '1990'
        }
        self.invalid_data = {
            'birthday': 'not a date'
        }

        self.message = {
            'birthday': {
                'date': 'date format is not ok'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())
        self.assertDictEqual(validator.get_message(), self.message)
