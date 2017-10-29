# PROJECT : django-contrib-validator
# TIME : 17-9-11 下午3:00
# AUTHOR : Younger Shen
# EMAIL : younger.x.shen@gmail.com
import datetime
from copy import deepcopy
from django.utils.translation import ugettext as _


class RuleNotFoundError(Exception):

    message = _('{NAME} rule not found error')

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.message.format(NAME=self.name)


class BaseRule:
    name = 'base rule name'
    message = _('i am the base rule message, you never see me bro')

    def __init__(self, name, value, *args, message=None):
        self.name = name
        self.value = value
        self.args = args
        self.status = True
        self.message = message if message else self.message

    def check(self):
        self.check_value() if self.value else self.check_null()

    def check_value(self):
        pass

    def check_null(self):
        pass

    def get_status(self):
        return self.status

    def get_message(self):
        return self.message


class Date(BaseRule):
    message = _('{FIELD} field is not a valid date format as xxxx-xx-xx')
    date_format = '%Y-%m-%d'

    def get_format(self):
        print('test')
        print(self.args)
        return self.args[0] if 1 == len(self.args) else self.date_format

    def check_value(self):
        date_format = self.get_format()
        try:
            datetime.datetime.strptime(self.value, date_format)
        except ValueError:
            self.status = False

    def get_message(self):
        return self.message.format(FIELD=self.name)


class DateTime(BaseRule):
    message = _('{FIELD} field is not a valid datetime format as xxxx-xx-xx xx:xx:xx')
    datetime_format = '%Y-%m-%d %H-%M-%S'

    def get_datetime_format(self):
        return self.args[0] if 1 == len(self.args) else self.datetime_format

    def check_value(self):
        datetime_format = self.get_datetime_format()
        try:
            datetime.datetime.strptime(self.value, datetime_format)
        except ValueError:
            self.status = False

    def get_message(self):
        return self.message.format(FIELD=self.name)


class DateTimeBefore(BaseRule):
    pass


class DatetTimeAfter(BaseRule):
    pass


class Required(BaseRule):
    message = '{FIELD} field is required'

    def check_null(self):
        self.status = False

    def get_message(self):
        return self.message.format(FIELD=self.name)


class Accepted(BaseRule):
    message = '{FIELD} field must in which of : yes or no'
    flag = ['yes', 'no']

    def check_value(self):
        self.status = False if self.value.lower() not in self.flag else True

    def get_message(self):
        return self.message.format(FIELD=self.name)


class MetaValidator(type):
    def __new__(mcs, *args, **kwargs):
        name, base, attrs = args
        attrs.update({'validation': mcs.get_attrs(attrs)})
        return super().__new__(mcs, *args)

    @staticmethod
    def get_attrs(attrs):
        return dict((k, v) for k, v in attrs.items() if not k.startswith('__') and isinstance(v, str))


class Validator(metaclass=MetaValidator):

    def __init__(self, data, request=None, extra_rules=None):
        self.data = deepcopy(data)
        self.request = request
        self.extra_rules = extra_rules
        self.status = True
        self.message = {}
        self.validate_message = {}

    def validate(self):
        validation = self._get_validation()
        self._validate(validation)
        return self.status

    def get(self, name, default=None):
        return self.data.get(name, default)

    def get_status(self):
        return self.status

    def get_message(self):
        return self.validate_message

    def set_message(self, name, rule, message):
        self.validate_message.update({name: {}}) if name not in self.validate_message.keys() else None
        self.validate_message[name].update({rule: message})

    def _validate(self, validation):
        for item in validation:
            name = item.get('name', '')
            value = item.get('value', '')
            rules = item.get('rules', [])
            [self._check_rule(rule, name, value) for rule in rules]

    def _get_rule(self, rule_info, name, value):
        rule_name = rule_info.get('name')
        params = rule_info.get('params')
        rule_class = self._get_origin_rule(rule_name)
        message = self.message.get(name, {}).get(rule_name, None)
        instance = rule_class(name, value, *params, message=message)
        return instance

    def _get_origin_rule(self, name):
        rule = self.extra_rules.get(name, None) if self.extra_rules else default_rules.get(name, None)
        if not rule:
            raise RuleNotFoundError(name)
        else:
            return rule

    def _check_rule(self, rule_info, name, value):
        rule = self._get_rule(rule_info, name, value)
        rule.check()
        if not rule.get_status():
            self.status = False
            self.set_message(name, rule_info.get('name'), rule.get_message())

    def _get_validation(self):
        ret = []
        for name, validation in self.validation.items():
            rules = self._get_rules(validation)
            value = self.get(name)
            data = {'name': name, 'value': value, 'rules': list(rules)}
            ret.append(data)
        return ret

    def _get_rules(self, validation):
        rules = map(self._get_rule_info, validation.split('|'))
        return rules

    @staticmethod
    def _get_rule_info(rule):
        info = list(map(lambda s: s.strip(), rule.split(':')))
        name = info[0]
        params = list(map(lambda s: s.strip(), ''.join(info[1:]).split(',')))
        params = params if len(params) > 0 and params[0] is not None else ()
        rules = {'name': name, 'params': params}
        return rules


default_rules = {
    'required': Required,
    'accepted': Accepted,
    'date': Date,
    'datetime': DateTime
}

