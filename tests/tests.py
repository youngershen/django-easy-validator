# PROJECT : django-easy-validator
# TIME    : 18-1-2 上午9:44
# AUTHOR  : 申延刚 <Younger Shen>
# EMAIL   : younger.shen@hotmail.com
# PHONE   : 13811754531
# WECHAT  : 13811754531
# WEBSITE : www.punkcoder.cn

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


class DateBefore(Validator):
    expired_at = 'date_before:1990-12-12'
    message = {
        'expired_at': {
            'date_before': 'date is not before 1990-12-12'
        }
    }


class DateBeforeCustom(Validator):
    expired_at = 'date_before:1990,%Y,%Y'
    message = {
        'expired_at': {
            'date_before': 'date is not before 1990'
        }
    }


class DateAfter(Validator):
    due_at = 'date_after:1990-12-12'
    message = {
        'due_at': {
            'date_after': 'date is not after 1990-12-12'
        }
    }


class DateAfterCustom(Validator):
    due_at = 'date_after:1990,%Y,%Y'
    message = {
        'due_at': {
            'date_after': 'date is not after 1990'
        }
    }


class DateRange(Validator):
    period = 'date_range:1990-12-12, 1991-12-12'
    message = {
        'period': {
            'date_range': 'date is not in range of {BEGIN} to {END}'
        }
    }


class Datetime(Validator):
    now = 'datetime'
    message = {
        'now': {
            'datetime': 'it is not a datetime format string'
        }
    }


class DatetimeBefore(Validator):
    due_at = 'datetime_before:1990-12-12 15:31:10'
    message = {
        'due_at': {
            'datetime_before': 'the input is not before {DATETIME}'
        }
    }


class DatetimeAfter(Validator):
    after_at = 'datetime_after:1990-12-12 15:31:10'
    message = {
        'after_at': {
            'datetime_after': 'the input is not after {DATETIME}'
        }
    }


class DatetimeRange(Validator):
    range_at = 'datetime_range:1990-12-12 15:31:10,1991-12-12 15:31:10'
    message = {
        'range_at': {
            'datetime_range': 'the input is not after {BEGIN} to {END}'
        }
    }


class ActiveUrl(Validator):
    url = 'active_url'
    message = {
        'url': {
            'active_url': 'it is not a active url'
        }
    }


class Numberic(Validator):
    number = 'numberic'
    message = {
        'number': {
            'numberic': '{VALUE} of number is not numberic'
        }
    }


class Digits(Validator):
    card = 'digits'
    message = {
        'card': {
            'digits': '{VALUE} of card is not digits'
        }
    }


class Regex(Validator):
    parse_args = False
    identity = 'regex:[0-9a-z]{3,5}'
    message = {
        'identity': {
            'regex': '{VALUE} of identity is not match the pattern {REGEX}'
        }
    }


class Email(Validator):
    email = 'email'
    message = {
        'email': {
            'email': '{VALUE} is not an email address'
        }
    }


class MinLength(Validator):
    username = 'min_length:4'
    message = {
        'username': {
            'min_length': '{VALUE} of username is shotter than 4'
        }
    }


class MaxLength(Validator):
    username = 'max_length:7'
    message = {
        'username': {
            'max_length': '{VALUE} of username is longger than 7'
        }
    }


class IDS(Validator):
    ids = 'ids'
    message = {
        'ids': {
            'ids': '{VALUE} of ids is not a id series'
        }
    }


class Cellphone(Validator):
    cellphone = 'cellphone'
    message = {
        'cellphone': {
            'cellphone': '{VALUE} is not a cellphone number'
        }
    }


class Alphabet(Validator):
    alphabet = 'alphabet'
    message = {
        'alphabet': {
            'alphabet': '{VALUE} of alphabet is not alphabet'
        }
    }


class Switch(Validator):
    accepted = 'switch:ok,good,awesome'
    message = {
        'accepted': {
            'switch': '{VALUE} of accepted is not in [{SWITCH}]'
        }
    }


class Unique(Validator):
    user_id = 'unique:AUTH_USER_MODEL,id'
    message = {
        'user_id': {
            'unique': '{VALUE} of {MODEL} with id is not unique'
        }
    }

# =====================================================================


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


class DateBeforeTestCase(TestCase):
    def setUp(self):
        self.validator = DateBefore
        self.valid_data = {
            'expired_at': '1982-11-30'
        }

        self.invalid_data = {
            'expired_at': '1991-04-25'
        }

        self.message = {
            'expired_at': {
                'date_before': 'date is not before 1990-12-12'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())
        self.assertDictEqual(self.message, validator.get_message())


class DateBeforeCustomTestCase(TestCase):
    def setUp(self):
        self.validator = DateBeforeCustom
        self.valid_data = {
            'expired_at': '1989'
        }
        self.invalid_data = {
            'expired_at': '1991'
        }
        self.message = {
            'expired_at': {
                'date_before': 'date is not before 1990'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())
        self.assertDictEqual(self.message, validator.get_message())


class DateAfterTestCase(TestCase):
    def setUp(self):
        self.validator = DateAfter
        self.valid_data = {
            'due_at': '1991-04-25'
        }
        self.invalid_data = {
            'due_at': '1982-11-30'
        }
        self.message = {
            'due_at': {
                'date_after': 'date is not after 1990-12-12'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())
        self.assertDictEqual(validator.get_message(), self.message)


class DateAfterCustomTestCase(TestCase):
    def setUp(self):
        self.validator = DateAfterCustom
        self.valid_data = {
            'due_at': '1991'
        }
        self.invalid_data = {
            'due_at': '1989'
        }
        self.message = {
            'due_at': {
                'date_after': 'date is not after 1990'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())
        self.assertDictEqual(validator.get_message(), self.message)


class DateRangeTestCase(TestCase):
    def setUp(self):
        self.validator = DateRange
        self.valid_data = {
            'period': '1991-01-01'
        }

        self.invalid_data = {
            'period': '1992-12-12'
        }

        self.message = {
            'period': {
                'date_range': 'date is not in range of 1990-12-12 to 1991-12-12'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())
        message = validator.get_message()
        self.assertDictEqual(self.message, message)


class DatetimeTestCase(TestCase):
    def setUp(self):
        self.validator = Datetime
        self.valid_data = {
            'now': '1987-10-5 12:55:01'
        }
        self.invalid_data = {
            'now': 'not a datetime string'
        }

        self.message = {
            'now': {
                'datetime': 'it is not a datetime format string'
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


class DatetimeBeforeTestCase(TestCase):
    def setUp(self):
        self.validator = DatetimeBefore
        self.valid_data = {
            'due_at': '1989-11-11 12:12:00'
        }
        self.invalid_data = {
            'due_at': '2018-06-01 12:55:01'
        }

        self.message = {
            'due_at': {
                'datetime_before': 'the input is not before 1990-12-12 15:31:10'
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


class DatetimeAfterTestCase(TestCase):
    def setUp(self):
        self.validator = DatetimeAfter
        self.valid_data = {
            'after_at': '2011-11-11 12:12:00'
        }
        self.invalid_data = {
            'after_at': '1955-11-11 12:12:00'
        }
        self.message = {
            'after_at': {
                'datetime_after': 'the input is not after 1990-12-12 15:31:10'
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


class DatetimeRangeTestCase(TestCase):
    def setUp(self):
        self.validator = DatetimeRange
        self.valid_data = {
            'range_at': '1991-01-12 15:31:10'
        }
        self.invalid_data = {
            'range_at': '1988-01-12 15:31:10'
        }

        self.message = {
            'range_at': {
                'datetime_range': 'the input is not after 1990-12-12 15:31:10 to 1991-12-12 15:31:10'
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


class ActiveUrlTestCase(TestCase):
    def setUp(self):
        self.validator = ActiveUrl
        self.valid_data = {
            'url': 'baidu.com'
        }
        self.invalid_data = {
            'url': 'www.sfsdf.sdffs'
        }
        self.message = {
            'url': {
                'active_url': 'it is not a active url'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())


class NumberciTestCase(TestCase):
    def setUp(self):
        self.validator = Numberic
        self.valid_data = {
            'number': '123'
        }
        self.invalid_data = {
            'number': 'abcdef'
        }

        self.message = {
            'number': {
                'numberic': 'abcdef of number is not numberic'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def tst_invalid(self):
        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())
        message = validator.get_message()
        self.assertDictEqual(message, self.message)


class DigitsTestCase(TestCase):
    def setUp(self):
        self.validator = Digits
        self.valid_data = {
            'card': '12345'
        }
        self.invalid_data = {
            'card': 'abcdef'
        }
        self.message = {
            'card': {
                'digits': 'abcdef of card is not digits'
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


class RegexTestCase(TestCase):
    def setUp(self):
        self.validator = Regex
        self.valid_data = {
            'identity': 'ab12'
        }
        self.invalid_data = {
            'identity': '1'
        }
        self.message = {
            'identity': {
                'regex': '1 of identity is not match the pattern [0-9a-z]{3,5}'
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


class EmailTestCase(TestCase):
    def setUp(self):
        self.validator = Email
        self.valid_data = {
            'email': 'younger.shen@hotmail.com'
        }
        self.invalid_data = {
            'email': 'i am a little bear'
        }
        self.message = {
            'email': {
                'email': 'i am a little bear is not an email address'
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


class MinLengthTestCase(TestCase):
    def setUp(self):
        self.validator = MinLength
        self.valid_data = {
            'username': 'abacdef'
        }
        self.invalid_data = {
            'username': 'a'
        }
        self.message = {
            'username': {
                'min_length': 'a of username is shotter than 4'
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


class MaxLengthTestCase(TestCase):
    def setUp(self):
        self.validator = MaxLength
        self.valid_data = {
            'username': 'abacde'
        }
        self.invalid_data = {
            'username': 'abcdefgh'
        }
        self.message = {
            'username': {
                'max_length': 'abcdefgh of username is longger than 7'
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


class IDSTestCase(TestCase):
    def setUp(self):
        self.validator = IDS
        self.valid_data = {
            'ids': '1,2,3,4'
        }
        self.invalid_data = {
            'ids': 'a,b,c,d'
        }
        self.message = {
            'ids': {
                'ids': 'a,b,c,d of ids is not a id series'
            }
        }

    def test_valid(self):
        validator = IDS(self.valid_data)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        validator = IDS(self.invalid_data)
        self.assertFalse(validator.validate())
        message = validator.get_message()
        self.assertDictEqual(message, self.message)


class CellphoneTestCase(TestCase):
    def setUp(self):
        self.validator = Cellphone
        self.valid_data = {
            'cellphone': '13811754531'
        }

        self.invalid_data = {
            '123456789123456789'
        }

        self.message = {
            'cellphone': {
                'cellphone': '123456789123456789 is not a cellphone number'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def tst_invalid(self):
        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())
        message = validator.get_message()
        self.assertDictEqual(message, self.message)


class AlphabetTestCase(TestCase):
    def setUp(self):
        self.validator = Alphabet
        self.valid_data = {
            'alphabet': 'abcdef'
        }
        self.invalid_data = {
            'alphabet': '123456'
        }

        self.message = {
            'alphabet': {
                'alphabet': '123456 of alphabet is not alphabet'
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


class SwitchTestCase(TestCase):
    def setUp(self):
        self.validator = Switch
        self.valid_data = {
            'accepted': 'ok'
        }

        self.invalid_data = {
            'accepted': 'bad'
        }
        self.message = {
            'accepted': {
                'switch': 'bad of accepted is not in [ok,good,awesome]'
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


class UniqueTestCase(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        User.objects.create_user('test', 'test')

        self.validator = Unique
        self.valid_data = {
            'user_id': '2'
        }
        self.invalid_data = {
            'user_id': '1'
        }

        self.message = {
            'user_id': {
                'unique': '1 of AUTH_USER_MODEL with id is not unique'
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
