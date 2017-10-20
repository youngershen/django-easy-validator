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

    def test_required(self):
        self.assertTrue(self.required_valid.validate())
        self.assertFalse(self.required_empty.validate())
        message = self.required_empty.get_message()
        self.assertDictEqual(message, {'username': {'required': 'username field is required'}})

    def test_accepted(self):
        self.assertTrue(self.accepted_valid.validate())
        self.assertFalse(self.accepted_invalid1.validate())
        message = self.accepted_invalid1.get_message()
        self.assertDictEqual(message, {'term': {'required': 'term field is required'},
                                       'policy': {'accepted': 'policy field must in which of : yes or no'}})
        self.assertFalse(self.accepted_invalid2.validate())
        message = self.accepted_invalid2.get_message()
        print(message)
        self.assertDictEqual(message, {'term': {'accepted': 'term field must in which of : yes or no'},
                                       'policy': {'accepted': 'policy field must in which of : yes or no'}})
