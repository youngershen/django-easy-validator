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
            'required': _('用户名不能为空')
        }
    }

    def check(self):
        username = self.get('username')
        if 'test' == username:
            self.code = 0
            self.status = True
        else:
            self.code = 1
            self.status = False
