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
        'username':
            {
                'required': _('用户名不能为空')
            }
    }

    info = {
        0: _('创建用户成功'),
        1: _('用户名格式错误'),
    }

    def check(self):
        self.code = 0
        pass


class RequiredValidator2(Validator):
    username = 'required'

    message = {
        'username':
            {
                'required': _('用户名不能为空2')
            }
    }

    info = {
        0: _('创建用户成功2'),
        1: _('用户名格式错误2'),
    }

    def check(self):
        self.code = 0
        pass


class Required(TestCase):
    def setUp(self):
        self.data1 = {
            'username': 'huahua'
        }

        self.data2 = {
            'username': ''
        }

    def test_required(self):
        validator = RequiredValidator(self.data1, None)
        status, code, message, info = validator.validate()

        assert status
        assert code == 0
        assert not message
        assert info == '创建用户成功'

        validator = RequiredValidator2(self.data2, None)
        status, code, message, info = validator.validate()
        assert not status
        assert code == 0
        assert message
        assert not info
