# Project: django-easy-validator
# File : simple.py
# Date : 2021/5/11 10:05
# Author: Younger Shen <申延刚>
# Web: https://github.com/youngershen
# Cell: 13811754531
# Email : shenyangang@163.com
from validator import Validator


class PrintableASCIIValidator(Validator):
    username = 'pascii:true'


if __name__ == '__main__':
    data = {
        'username': '  @  '
    }

    v = PrintableASCIIValidator(data)

    print(v.validate())
