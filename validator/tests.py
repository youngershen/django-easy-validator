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


class Test(TestCase):
    def setUp(self):
        self.setup_required()

    def tearDown(self):
        pass

    def setup_required(self):
        data_valid = {
            'username': 'test',
        }

        data_empty = {
            'username': ''
        }

        self.validator_valid = RequiredValidator(data_valid, [])
        self.validator_empty = RequiredValidator(data_empty, [])

    def test_required(self):
        self.assertFalse(self.validator_empty.validate())
        message = self.validator_empty.get_message()
        self.assertDictEqual(message, {'username': {'required': 'username is required'}})

        self.assertFalse(self.validator_empty.validate())
        self.assertDictEqual(message, {'username': {'required': 'username is required'}})
