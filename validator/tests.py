# PROJECT : validator
# TIME : 17-9-16 上午10:14
# AUTHOR : Younger Shen
# EMAIL : younger.x.shen@gmail.com
from django.utils.translation import ugettext as _
from django.test import TestCase
from validator import Validator


class RequiredValidator(Validator):
    username = 'required'
    message = {
        'username': {
            'required': _('username is required')
        }
    }

    info = {
        0: _('you succeed'),
        1: _('you failed')
    }

    def check(self):
        username = self.get('username')
        if 'test' == username:
            self.code = 0
            self.status = True
        else:
            self.code = 1
            self.status = False


class Test(TestCase):
    def setUp(self):
        self.setup_required()

    def tearDown(self):
        pass

    def setup_required(self):
        data_valid = {
            'username': 'test',
        }

        data_invalid = {
            'username': 'hello'
        }

        data_empty = {
            'username': ''
        }

        self.validator_valid = RequiredValidator(data_valid, [])
        self.validator_invalid = RequiredValidator(data_invalid, [])
        self.validator_empty = RequiredValidator(data_empty, [])

    def test_required(self):
        status, code, message, info = self.validator_valid.validate()
        assert status
        assert 0 == code
        assert not message
        assert 'you succeed' == info

        status, code, message, info = self.validator_invalid.validate()
        assert not status
        assert 1 == code
        assert not message
        assert 'you failed' == info

        status, code, message, info = self.validator_empty.validate()
        assert not status
        assert -1 == code
        assert 'username is required' == message['username']['required']
        assert 'data is invalid' == info
