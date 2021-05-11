# PROJECT : django-easy-validator
# TIME    : 18-1-2 上午9:44
# AUTHOR : Younger Shen
# EMAIL : younger.x.shen@gmail.com
# CELL : 13811754531
# WECHAT : 13811754531
# https://github.com/youngershen/

from io import BytesIO
from django.test import TestCase
from django.core.files.uploadedfile import InMemoryUploadedFile
from validator import Validator, BaseRule


class AlphaNumber(Validator):
    code = 'alpha_number'

    message = {
        'code': {
            'alpha_number': '{VALUE} is not a alpha number type series.'
        }
    }


class Array(Validator):
    ids = 'array'
    message = {
        'ids': {
            'array': '{VALUE} is not a array type series.'
        }
    }


class Between(Validator):
    age = 'between:10,20'
    message = {
        'age': {
            'between': '{VALUE} is not between 10 to 20'
        }
    }


class Boolean(Validator):
    remember_me = 'boolean'
    message = {
        'remember_me': {
            'boolean': '{VALUE} is not a boolean type value.'
        }
    }


class TestRule(BaseRule):
    name = 'test_rule'
    message = 'test custom rule failed'
    description = 'just for custom rule test'

    def check_value(self):
        self.status = True if self.field_value == 'test' else False

    def check_null(self):
        pass


class TestRuleValidator(Validator):
    name = 'test_rule'


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


class Size(Validator):
    username = 'size:string,5'
    number = 'size:number,5'
    profile = 'size:array,2'
    avatar = 'size:file,13.903'

    message = {
        'username': {
            'size': 'size of username is not equals to 5'
        },
        'number': {
            'size': 'size of number is not equals to 5'
        },
        'profile': {
            'size': 'size of profile is not equals to 2'
        },
        'avatar': {
            'size': 'size of avatar is not equals to 13.903KB'
        }
    }


class Min(Validator):
    age = 'min:number,15'

    message = {
        'age': {
            'min': 'sorry we do not support service to people who is under 15.'
        }
    }


class Max(Validator):
    age = 'max:number,50'
    message = {
        'age': {
            'max': 'sorry we do not support service to people who is older than 50.'
        }
    }


class File(Validator):
    file = 'file:png,jpeg,zip,rar'

    message = {
        'file': {
            'file': 'file is not allowed to upload'
        }
    }


class AlphaDash(Validator):
    username = 'alpha_dash'

    message = {
        'username': {
            'alpha_dash': 'username should only includes alphabet and dash characters.'
        }
    }


class Username(Validator):
    username = 'username'
    message = {
        'username': {
            'username': 'the input {VALUE} is not a proper username.'
        }
    }


class PasswordLow(Validator):
    password = 'password:low'
    message = {
        'password': {
            'password': 'the input is not a proper password.'
        }
    }


class PasswordMiddle(Validator):
    password = 'password:middle'
    message = {
        'password': {
            'password': 'the input is not a proper password.'
        }
    }


class PasswordHigh(Validator):
    password = 'password:high'
    message = {
        'password': {
            'password': 'the input is not a proper password.'
        }
    }


class ASCII(Validator):
    seq = 'ascii'


class Same(Validator):
    password = 'required'
    password_confirm = 'required|same:password'


class Decimal(Validator):
    price = 'required|decimal'


class Exist(Validator):
    username = 'required|exist:AUTH_USER_MODEL,username'


class UniqueAgainst(Validator):
    username = 'required|unique_against:AUTH_USER_MODEL, username, youngershen'


class PrintableASCII(Validator):
    username = 'pascii'

    message = {
        'username': {
            'pascii': '用户名不能为空'
        }
    }


class PrintableASCIINoBlank(Validator):
    username = 'pascii:true'

    message = {
        'username': {
            'pascii': '用户名不能为空'
        }
    }
# ======================================================================================================================


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


class SizeTestCase(TestCase):
    def setUp(self):
        self.avatar = self.get_avatar()
        self.validator = Size

        self.valid_data = {
            'username': 'abcde',
            'number': '5',
            'profile': 'age,12',
            'avatar': self.avatar
        }

        self.invalid_data = {
            'username': '',
            'number': '',
            'profile': '',
            'avatar': ''
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def get_avatar(self):
        buffer = BytesIO()
        self.get_temp_file(buffer)
        avatar = InMemoryUploadedFile(
            file=buffer,
            field_name='avatar',
            name='avatar',
            size=len(buffer.getvalue()),
            charset=None,
            content_type='image/jpeg'
        )
        self.assertTrue(avatar.content_type)
        return avatar

    @staticmethod
    def get_temp_file(buffer):
        with open('tests/assets/linux.jpeg', mode='rb') as f:
            buffer.write(f.read())


class MinTestCase(TestCase):
    def setUp(self):
        self.validator = Min
        self.valid_data = {
            'age': 20
        }
        self.invalid_data = {
            'age': 10
        }

        self.message = {
            'age': {
                'min': 'sorry we do not support service to people who is under 15.'
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


class AlphaDashTestCase(TestCase):
    def setUp(self):
        self.validator = AlphaDash
        self.valid_data = {
            'username': 'abc_def'
        }
        self.invalid_data = {
            'username': '#%#@'
        }
        self.message = {
            'username': {
                'alpha_dash': 'username should only includes alphabet and dash characters.'
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


class MaxTestCase(TestCase):
    def setUp(self):
        self.validator = Max
        self.valid_data = {
            'age': 15
        }
        self.invalid_data = {
            'age': 55
        }
        self.message = {
            'age': {
                'max': 'sorry we do not support service to people who is older than 50.'
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


class FileTestCase(TestCase):
    def setUp(self):
        self.validator = File
        self.valid_data = {
            'file': self.get_file()
        }
        self.invalid_data = {
            'file': self.get_file('tgz')
        }

        self.message = {
            'file': {
                'file': 'file is not allowed to upload'
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

    @staticmethod
    def get_file(_type='jpeg'):
        buffer = BytesIO()
        with open('tests/assets/linux.' + _type, mode='rb') as f:
            buffer.write(f.read())

        file = InMemoryUploadedFile(
            file=buffer,
            field_name='file',
            name='file.' + _type,
            size=len(buffer.getvalue()),
            charset=None,
            content_type='image/jpeg'
        )
        return file


class CustomRuleTestCase(TestCase):
    def setUp(self):
        self.extra_rules = {
            TestRule.get_name(): TestRule
        }
        self.validator = TestRuleValidator
        self.message = {
            'name': {
                'test_rule': 'test custom rule failed'
            }
        }
        self.valid_data = {
            'name': 'test',
        }
        self.invalid_data = {
            'name': 'toast'
        }

    def test_valid(self):
        validator = self.validator(extra_rules=self.extra_rules, data=self.valid_data)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        validator = self.validator(extra_rules=self.extra_rules, data=self.invalid_data)
        self.assertFalse(validator.validate())
        message = validator.get_message()
        self.assertDictEqual(message, self.message)


class UsernameTestCase(TestCase):
    def setUp(self):
        self.validator = Username
        self.valid_data = {
            'username': 'abc8848cba'
        }
        self.invalid_data = {
            'username': '123ABCdef'
        }
        self.message = {
            'username': {
                'username': 'the input 123ABCdef is not a proper username.'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        valiadtor = self.validator(self.invalid_data)
        self.assertFalse(valiadtor.validate())
        message = valiadtor.get_message()
        self.assertDictEqual(message, self.message)


class PasswordTestCase(TestCase):
    def setUp(self):
        self.validator1 = PasswordLow
        self.validator2 = PasswordMiddle
        self.validator3 = PasswordHigh

        self.valid_data1 = {
            'password': '1234567设定'
        }
        self.valid_data2 = {
            'password': 'abcDEF123'
        }
        self.valid_data3 = {
            'password': 'ABCdef123!@#'
        }
        self.invalid_data1 = {
            'password': '123'
        }
        self.invalid_data2 = {
            'password': 'abcdef123'
        }
        self.invalid_data3 = {
            'password': 'abcdef1234'
        }

    def test_low(self):
        validator = self.validator1(self.valid_data1)
        self.assertTrue(validator.validate())

        validator = self.validator1(self.invalid_data1)
        self.assertFalse(validator.validate())

    def test_middle(self):
        validator = self.validator2(self.valid_data2)
        self.assertTrue(validator.validate())

        validator = self.validator2(self.invalid_data2)
        self.assertFalse(validator.validate())

    def test_high(self):
        validator = self.validator3(self.valid_data3)
        self.assertTrue(validator.validate())

        validator = self.validator3(self.invalid_data3)
        self.assertFalse(validator.validate())


class ASCIITestCase(TestCase):
    def setUp(self):
        self.validator = ASCII
        self.valid_data = {
            'seq': 'a   '
        }
        self.invalid_data = {
            'seq': '你好世界'
        }

        self.message = {
            'seq': {
                'ascii': 'the input 你好世界 value is not a proper ASCII character.'
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


class BooleanTestCase(TestCase):
    def setUp(self):
        self.validator = Boolean
        self.valid_data = {
            'remember_me': 'true'
        }

        self.invalid_data = {
            'remember_me': 'haha'
        }

        self.message = {
            'remember_me': {
                'boolean': 'haha is not a boolean type value.'
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


class BetweenTestCase(TestCase):
    def setUp(self):
        self.validator = Between
        self.valid_data = {
            'age': 15
        }
        self.invalid_data = {
            'age': 25
        }
        self.message = {
            'age': {
                'between': '25 is not between 10 to 20'
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


class ArrayTestCase(TestCase):
    def setUp(self):
        self.validator = Array
        self.valid_data = {
            'ids': '1, 2, 3, 4'
        }
        self.invalid_data = {
            'ids': 'abcdef'
        }

        self.message = {
            'ids': {
                'array': 'abcdef is not a array type series.'
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


class AlphaNumberTest(TestCase):
    def setUp(self):
        self.validator = AlphaNumber
        self.valid_data = {
            'code': 'abc123'
        }
        self.invalid_data = {
            'code': '密码'
        }
        self.message = {
            'code': {
                'alpha_number': '密码 is not a alpha number type series.'
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


class SameTestCase(TestCase):
    def setUp(self):
        self.validator = Same
        self.valid_data = {
            'password': 'abcd1234',
            'password_confirm': 'abcd1234'
        }

        self.invalid_data = {
            'password': 'abcd',
            'password_confirm': '1234'
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())


class DecimalTestCase(TestCase):
    def setUp(self):
        self.validator = Decimal
        self.valid_data = {
            'price': 123.456
        }
        self.invalid_data = {
            'price': 'abcdef'
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())


class ExistTestCase(TestCase):
    def setUp(self):
        self.setup_users()
        self.validator = Exist
        self.valid_data = {
            'username': 'youngershen'
        }
        self.invalid_data = {
            'username': 'bear'
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())

    @staticmethod
    def setup_users():
        from django.contrib.auth.models import User
        User.objects.create_user(username='youngershen',
                                 email='shenyangang@163.com',
                                 password='123456789')


class UniqueAgainstTestCase(TestCase):
    def setUp(self):
        self.setup_users()
        self.validator = UniqueAgainst
        self.valid_data = {
            'username': 'youngershen'
        }
        self.invalid_data = {
            'username': 'bear'
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())

    @staticmethod
    def setup_users():
        from django.contrib.auth.models import User
        User.objects.create_user(username='youngershen',
                                 email='shenyangang@163.com',
                                 password='123456789')

        User.objects.create_user(username='bear',
                                 email='shenyangang@163.com',
                                 password='123456789')


class PrintableASCIITestCase(TestCase):
    def setUp(self):
        self.validator = PrintableASCII
        self.valid_data = {
            'username': 'abcdef@123456'
        }
        self.invalid_data = {
            'username': chr(555)
        }
        self.valid_data_blank = {
            'username': '       '
        }
        self.message = {
            'username': {
                'pascii': '用户名不能为空'
            }
        }

    def test_valid(self):
        validator = self.validator(self.valid_data)
        self.assertTrue(validator.validate())

        validator = self.validator(self.valid_data_blank)
        self.assertTrue(validator.validate())

    def test_invalid(self):
        validator = self.validator(self.invalid_data)
        self.assertFalse(validator.validate())
        message = validator.get_message()
        self.assertDictEqual(message, self.message)

        validator = self.validator(self.valid_data_blank)
        self.assertTrue(validator.validate())


class PrintableASCIINoBlankTestCase(TestCase):
    def setUp(self):
        self.validator = PrintableASCIINoBlank
        self.valid_data = {
            'username': 'abcdef@123456'
        }
        self.invalid_data = {
            'username': chr(555)
        }
        self.invalid_data_blank = {
            'username': '       '
        }
        self.message = {
            'username': {
                'pascii': '用户名不能为空'
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

        validator = self.validator(self.invalid_data_blank)
        self.assertFalse(validator.validate())
        message = validator.get_message()
        self.assertDictEqual(message, self.message)
