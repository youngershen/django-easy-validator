# PROJECT : validator
# TIME : 17-9-11 下午3:00
# AUTHOR : Younger Shen
# EMAIL : younger.x.shen@gmail.com


class BaseValidator(type):

    def __init__(cls):
        super().__init__()

    def __new__(mcs, *args, **kwargs):
        pass


class Validator(metaclass=BaseValidator):
    pass
