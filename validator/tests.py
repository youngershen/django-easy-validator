# PROJECT : validator
# TIME : 17-9-16 上午10:14
# AUTHOR : Younger Shen
# EMAIL : younger.x.shen@gmail.com
from django.utils.translation import ugettext as _
from django.test import TestCase
from validator import Validator


class DefaultDatetimeValidator(Validator):
    created_at = 'required|datetime'

    message = {
        'created_at': {
            'required': _('created_at is required'),
            'datetime': _('created_at is not a valid datetime string')
        }
    }


class DatetimeValidator(DefaultDatetimeValidator):
    created_at = 'required|datetime'


class CustomDatetimeValidator(DatetimeValidator):
    created_at = 'required|datetime:%Y-%m-%d %H-%M-%S'

    message = {

    }


class DefaultDateValidator(Validator):
    birthday = 'required|date'

    message = {
        'birthday': {
            'required': _('birthday is required'),
            'date': _('birthday is not a valid date format string')
        }
    }


class DateValidator(DefaultDateValidator):
    birthday = 'required|date'


class CustomDateValidator(DefaultDateValidator):
    birthday = 'required|date:%Y'


class DefaultDatetimeValidator(Validator):
    expired_at = 'required|datetime'

    message = {
        'expired_at': {
            'required': _('expired_at is required'),
        }
    }


class RequiredValidator(Validator):
    username = 'required'

    message = {
        'username': {
            'required': _('username is required'),
        },
    }


class AcceptedValidator(Validator):
    term = 'required|accepted'
    policy = 'accepted'


class Test(TestCase):
    def setUp(self):
        self.setup_required()
        self.setup_accepted()
        self.setup_date()
        self.setup_datetime()

    def tearDown(self):
        pass

    def setup_required(self):
        data_valid = {
            'username': 'hello',
        }

        data_empty = {
            'username': '',
        }

        self.required_valid = RequiredValidator(data_valid)
        self.required_empty = RequiredValidator(data_empty)

    def setup_accepted(self):
        data_valid = {
            'term': 'yes',
            'policy': 'yes'
        }
        data_invalid1 = {
            'term': '',
            'policy': 'hello'
        }
        data_invalid2 = {
            'term': 'hello',
            'policy': 'hello'
        }

        self.accepted_valid = AcceptedValidator(data_valid)
        self.accepted_invalid1 = AcceptedValidator(data_invalid1)
        self.accepted_invalid2 = AcceptedValidator(data_invalid2)

    def setup_date(self):
        data_valid = {
            'birthday': '1990-12-12'
        }
        data_invalid = {
            'birthday': 'nonce'
        }

        data_empty = {
            'birthday': ''
        }

        data_custom = {
            'birthday': '1990'
        }

        data_custom_invalid = {
            'birthday': '1990-12-12'
        }

        data_custom_empty = {
            'birthday': ''
        }

        self.date_valid = DateValidator(data_valid)
        self.date_invalid = DateValidator(data_invalid)
        self.date_empty = DateValidator(data_empty)
        self.date_custom = CustomDateValidator(data_custom)
        self.date_custom_invalid = CustomDateValidator(data_custom_invalid)
        self.date_custom_empty = CustomDateValidator(data_custom_empty)

    def setup_datetime(self):
        data_valid = {
            'created_at': '1990-12-12 05:05:06'
        }
        self.datetime_valid = DatetimeValidator(data_valid)

        data_empty = {
            'created_at': ''
        }
        self.datetime_empty = DatetimeValidator(data_empty)

        data_invalid = {
            'created_at': 'test'
        }
        self.datetime_invalid = DatetimeValidator(data_invalid)

        custom_data_valid = {
            'created_at': '1999-11-11 05-05-06'
        }
        self.datetime_custom_valid = CustomDatetimeValidator(custom_data_valid)

        custom_data_invalid = {
            'created_at': '1991'
        }
        self.datetime_custom_invalid = CustomDatetimeValidator(custom_data_invalid)

    def test_required(self):
        self.assertTrue(self.required_valid.validate())
        self.assertFalse(self.required_empty.validate())
        message = self.required_empty.get_message()
        self.assertDictEqual(message, {'username': {'required': 'username is required'}})

    def test_accepted(self):
        self.assertTrue(self.accepted_valid.validate())
        self.assertFalse(self.accepted_invalid1.validate())
        message = self.accepted_invalid1.get_message()
        self.assertDictEqual(message, {'term': {'required': 'term field is required'},
                                       'policy': {'accepted': 'policy field must in which of : yes or no'}})
        self.assertFalse(self.accepted_invalid2.validate())
        message = self.accepted_invalid2.get_message()
        self.assertDictEqual(message, {'term': {'accepted': 'term field must in which of : yes or no'},
                                       'policy': {'accepted': 'policy field must in which of : yes or no'}})

    def test_date(self):
        self.assertTrue(self.date_valid.validate())
        self.assertFalse(self.date_invalid.validate())
        message = self.date_invalid.get_message()
        self.assertDictEqual(message, {
            'birthday': {
                'date': 'birthday is not a valid date format string'
            }
        })

        self.assertFalse(self.date_empty.validate())
        message = self.date_empty.get_message()
        self.assertDictEqual(message, {
            'birthday': {
                'required': 'birthday is required'
            }
        })

        self.assertTrue(self.date_custom.validate())
        self.assertFalse(self.date_custom_empty.validate())
        message = self.date_custom_empty.get_message()
        self.assertDictEqual(message, {
            'birthday': {
                'required': 'birthday is required'
            }
        })

        self.assertFalse(self.date_custom_invalid.validate())
        message = self.date_custom_invalid.get_message()
        self.assertDictEqual(message, {
            'birthday': {
                'date': 'birthday is not a valid date format string'
            }
        })

    def test_datetime(self):
        self.assertTrue(self.datetime_valid.validate())

        self.assertFalse(self.datetime_empty.validate())
        message = self.datetime_empty.get_message()
        self.assertDictEqual(message, {
            'created_at': {
                'required': 'created_at is required'
            }
        })

        self.assertFalse(self.datetime_invalid.validate())
        message = self.datetime_invalid.get_message()
        self.assertDictEqual(message, {
            'created_at': {
                'datetime': 'created_at is not a valid datetime string'
            }
        })

        self.assertTrue(self.datetime_custom_valid.validate())

        self.assertFalse(self.datetime_custom_invalid.validate())
        message = self.datetime_custom_invalid.get_message()
        self.assertDictEqual(message, {
            'created_at': {
                'datetime': 'created_at field is not a valid datetime format as %Y-%m-%d %H-%M-%S'
            }
        })
