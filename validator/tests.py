# PROJECT : validator
# TIME : 17-9-16 上午10:14
# AUTHOR : Younger Shen
# EMAIL : younger.x.shen@gmail.com
from django.utils.translation import ugettext as _
from django.test import TestCase
from validator import Validator


class RegexValidator(Validator):
    string = 'regex:abc'

    message = {
        'string': {
            'regex': _('the {VALUE} of field {FIELD} is not fix abc')
        }
    }


class DateRangeValidator(Validator):
    birthday = 'date_range:1990-12-12,1998-12-12'
    message = {
        'birthday': {
            'date_range': _('this is not my fucking date range')
        }
    }


class DateAfterValidator(Validator):
    birthday = 'date_after: 1990-12-12'
    message = {
        'birthday': {
            'date_after': _('this is not my birthday')
        }
    }


class DateBeforeValidator(Validator):
    birthday = 'date_before: 1990-12-12'
    message = {
        'birthday': {
            'date_before': _('this is not my birthday')
        }
    }


class ActiveURLValidator(Validator):
    url = 'active_url'
    message = {
        'url': {
            'active_url': _('{VALUE} is no a active url')
        }
    }


class NumbericValidator(Validator):
    number = 'numberic'
    message = {
        'number': {
            'numberic': _('{VALUE} is not a number')
        }
    }


class DigitsValidator(Validator):
    number = 'required|digits'

    message = {
        'number': {
            'required': _('number is required'),
            'digits': _('{VALUE} is not digits')
        }
    }


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
        self.setup_digits()
        self.setup_numberic()
        self.setup_active_url()
        self.setup_date_before()
        self.setup_date_after()
        self.setup_date_range()
        self.setup_regex()

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

    def setup_digits(self):
        data_valid_str = {'number': '0123456789'}
        self.digits_valid_str = DigitsValidator(data_valid_str)

        data_valid_int = {'number': 123456798}
        self.digits_valid_int = DigitsValidator(data_valid_int)

        data_invalid = {'number': 'abc1230'}
        self.digits_invalid = DigitsValidator(data_invalid)

    def setup_numberic(self):
        valid_data = {'number': 1234555}
        self.numberic_valid = NumbericValidator(valid_data)

        invalid_data = {'number': 'abc123'}
        self.numberic_invalid = NumbericValidator(invalid_data)

    def setup_active_url(self):
        active_url_valid = {
            'url': 'google.com'
        }
        self.valid_active_url = ActiveURLValidator(active_url_valid)

        active_url_invalid = {
            'url': 'not_a_domain.com'
        }
        self.invalid_active_url = ActiveURLValidator(active_url_invalid)

    def setup_date_before(self):
        valid_date_before = {
            'birthday': '1989-12-12'
        }

        self.valid_date_before = DateBeforeValidator(valid_date_before)

        invalid_date_before = {
            'birthday': '1999-12-12'
        }

        self.invalid_date_before = DateBeforeValidator(invalid_date_before)

    def setup_date_after(self):
        valid_date_after = {
            'birthday': '1991-12-12'
        }

        invalid_date_after = {
            'birthday': '1989-12-12'
        }
        self.valid_date_after = DateAfterValidator(valid_date_after);
        self.invalid_date_after = DateAfterValidator(invalid_date_after)

    def setup_date_range(self):
        valid_date_range = {
            'birthday': '1991-12-12'
        }

        invalid_date_range = {
            'birthday': '1988-12-12'
        }

        self.valid_date_range = DateRangeValidator(valid_date_range)
        self.invalid_date_range = DateRangeValidator(invalid_date_range)

    def setup_regex(self):
        valid_regex_data = {'string': 'abc'}
        invalid_regex_data = {'string': 'def'}

        self.valid_regex_validator = RegexValidator(valid_regex_data)
        self.invalid_regex_validator = RegexValidator(invalid_regex_data)

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
                                       'policy': {'accepted': 'hello of policy field must in which of : yes, no'}})
        self.assertFalse(self.accepted_invalid2.validate())
        message = self.accepted_invalid2.get_message()
        self.assertDictEqual(message, {'term': {'accepted': 'hello of term field must in which of : yes, no'},
                                       'policy': {'accepted': 'hello of policy field must in which of : yes, no'}})

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
                'datetime': '1991 of created_at field is not a valid datetime format as %Y-%m-%d %H-%M-%S'
            }
        })

    def test_digits(self):
        self.assertTrue(self.digits_valid_str.validate())
        self.assertTrue(self.digits_valid_int.validate())

        self.assertFalse(self.digits_invalid.validate())
        message = self.digits_invalid.get_message()
        self.assertDictEqual(message, {
            'number': {
                'digits': 'abc1230 is not digits'
            }
        })

    def test_numberic(self):
        self.assertTrue(self.numberic_valid.validate())

        self.assertFalse(self.numberic_invalid.validate())
        message = self.numberic_invalid.get_message()
        self.assertDictEqual(message, {
            'number': {
                'numberic': _('abc123 is not a number')
            }
        })

    def test_active_url(self):
        self.assertTrue(self.valid_active_url.validate())

        self.assertFalse(self.invalid_active_url.validate())
        message = self.invalid_active_url.get_message()
        self.assertDictEqual(message, {
            'url': {
                'active_url': 'not_a_domain.com is no a active url'
            }
        })

    def test_date_before(self):
        self.assertTrue(self.valid_date_before.validate())

        self.assertFalse(self.invalid_date_before.validate())
        message = self.invalid_date_before.get_message()
        self.assertDictEqual(message, {
            'birthday': {
                'date_before': 'this is not my birthday'
            }
        })

    def test_date_after(self):
        self.assertTrue(self.valid_date_after.validate())

        self.assertFalse(self.invalid_date_after.validate())
        message = self.invalid_date_after.get_message()
        self.assertDictEqual(message, {
            'birthday': {
                'date_after': 'this is not my birthday'
            }
        })

    def test_date_range(self):
        self.assertTrue(self.valid_date_range.validate())
        self.assertFalse(self.invalid_date_range.validate())
        message = self.invalid_date_range.get_message()
        self.assertDictEqual(message, {
            'birthday': {
                'date_range': 'this is not my fucking date range'
            }
        })

    def test_regex(self):
        self.assertTrue(self.valid_regex_validator.validate())
        self.assertFalse(self.invalid_regex_validator.validate())
        message = self.invalid_regex_validator.get_message()
        self.assertDictEqual(message, {
            'string': {
                'regex': 'the def of field string is not fix abc'
            }
        })

    def test_email(self):
        pass

    def test_min_length(self):
        pass

    def test_max_length(self):
        pass

    def test_ids(self):
        pass

    def test_cellphone(self):
        pass

    def test_alphabet(self):
        pass
