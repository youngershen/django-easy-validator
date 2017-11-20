# PROJECT : django-contrib-validator
# TIME : 17-9-11 下午3:00
# AUTHOR : Younger Shen
# EMAIL : younger.x.shen@gmail.com
import re
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
    name = 'base_rule'
    message = _('{VALUE} of {FIELD} field is match rule {RULE_NAME}.')

    def __init__(self, field_name, field_value, *args, message=None):
        self.field_name = field_name
        self.field_value = field_value
        self.args = args
        self.status = True
        self.message = message if message else self.message

    def check(self):
        self.check_value() if self.field_value else self.check_null()

    def check_value(self):
        pass

    def check_null(self):
        pass

    def get_status(self):
        return self.status

    def get_message(self):
        return self.message.format(FIELD=self.field_name, VALUE=self.field_value, RULE_NAME=self.name)

    @classmethod
    def get_name(cls):
        return cls.name


class Digits(BaseRule):
    name = 'digits'
    message = _('{VALUE} of {FIELD} is not match digits')

    def check_value(self):
        digits_regex = r'[0-9]+'
        self.status = True if re.match(digits_regex, str(self.field_value)) else False


class Numberic(BaseRule):
    name = 'numberic'
    message = _('{VALUE} of {FIELD} is not match numberic')

    def check_value(self):
        try:
            int(str(self.field_value))
        except ValueError:
            self.status = False
        else:
            self.status = True


class ActiveURL(BaseRule):
    name = 'active_url'
    message = '{FIELD field is not a active URL}'

    def check_value(self):
        pass


class Filled(BaseRule):
    name = 'filled'
    pass


class Date(BaseRule):
    name = 'date'
    message = _('{VALUE} of {FIELD} field is not a valid date format as {FORMAT_STR}')
    format_str = '%Y-%m-%d'

    def get_format(self):
        return self.args[0] if 1 == len(self.args) and self.args[0] else self.format_str

    def check_value(self):
        date_format = self.get_format()
        try:
            datetime.datetime.strptime(self.field_value, date_format)
        except ValueError:
            self.status = False

    def get_message(self):
        format_str = self.get_format()
        return self.message.format(FIELD=self.field_name,
                                   VALUE=self.field_value,
                                   FORMAT_STR=format_str,
                                   RULE_NAME=self.name)


class Datetime(BaseRule):
    name = 'datetime'
    message = _('{VALUE} of {FIELD} field is not a valid datetime format as {FORMAT_STR}')
    format_str = '%Y-%m-%d %H:%M:%S'

    def get_format(self):
        return self.args[0] if 1 == len(self.args) and self.args[0] else self.format_str

    def check_value(self):
        datetime_format = self.get_format()
        try:
            datetime.datetime.strptime(self.field_value, datetime_format)
        except ValueError:
            self.status = False

    def get_message(self):
        format_str = self.get_format()
        return self.message.format(FIELD=self.field_name,
                                   VALUE=self.field_value,
                                   FORMAT_STR=format_str,
                                   RULE_NAME=self.name)


class DateBefore(BaseRule):
    name = 'date_before'
    message = _('{VALUE} of {FIELD} is not before date {DATE}')
    field_format_str = '%Y-%m-%d'
    param_format_str = '%Y-%m-%d'

    def check_value(self):
        param_date = self._get_param_date()
        field_date = self._get_field_date()
        return field_date < param_date

    def _get_param_date(self):
        date_str = self.args[0] if len(self.args) == 1 else None
        date = datetime.datetime.strptime(date_str, self.param_format_str)
        return date

    def _get_field_date(self):
        date = datetime.datetime.strptime(self.field_value, self.field_format_str)
        return date

    def get_message(self):
        return self.message.format(VALUE=self.field_value,
                                   FIELD=self.field_name,
                                   DATE=self.args[0])


class DateAfter(BaseRule):
    name = 'date_after'
    message = _('{VALUE} of {FIELD} is not after date {DATE}')
    field_format_str = '%Y-%m-%d'
    param_format_str = '%Y-%m-%d'

    def check_value(self):
        param_date = self._get_param_date()
        field_date = self._get_field_date()
        return field_date > param_date

    def _get_param_date(self):
        date_str = self.args[0]
        date = datetime.datetime.strptime(date_str, self.param_format_str)
        return date

    def _get_field_date(self):
        date = datetime.datetime.strptime(self.field_value, self.field_format_str)
        return date

    def get_message(self):
        return self.message.format(VALUE=self.field_value,
                                   FIELD=self.field_name,
                                   DATE=self.args[0])


class DateRange(BaseRule):
    name = 'date_range'
    message = _('{VALUE} of {FIELD} is not in range date of {BEGIN} to {END}')
    field_format_str = '%Y-%m-%d'
    param_format_str = '%Y-%m-%d'

    def check_value(self):
        begin, end = self._get_param_date()
        date = self._get_field_date()
        return begin < date < end

    def _get_param_date(self):
        begin_date_str = self.args[0]
        begin_date = datetime.datetime.strptime(begin_date_str, self.param_format_str)

        end_date_str = self.args[1]
        end_date = datetime.datetime.strptime(end_date_str, self.param_format_str)

        return begin_date, end_date

    def _get_field_date(self):
        date = datetime.datetime.strptime(self.field_value, self.field_format_str)
        return date

    def get_message(self):
        return self.message.format(VALUE=self.field_value,
                                   FIELD=self.field_name,
                                   BEGIN=self.args[0],
                                   END=self.args[1])


class DateTimeBefore(BaseRule):
    name = 'datetime_before'
    message = _('{VALUE} of {FIELD} is not in range of {BEGIN} to {END}')
    format_str = ''


class DatetTimeAfter(BaseRule):
    name = 'datetime_after'
    pass


class DatetimeRange(BaseRule):
    name = 'datetime_range'


class Required(BaseRule):
    name = 'required'
    message = '{FIELD} field is required'

    def check_null(self):
        self.status = False


class Accepted(BaseRule):
    name = 'accepted'
    message = '{VALUE} of {FIELD} field must in which of : {FLAGS}'
    flag = ['yes', 'no']

    def get_flags(self):
        return ', '.join(self.flag)

    def check_value(self):
        self.status = False if self.field_value.lower() not in self.flag else True

    def get_message(self):
        return self.message.format(FIELD=self.field_name,
                                   VALUE=self.field_value,
                                   FLAGS=self.get_flags(),
                                   RULE_NAME=self.name)


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
        message = getattr(self, 'message', {}).get(name, {}).get(rule_name, None)
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
    Required.get_name(): Required,
    Accepted.get_name(): Accepted,
    Date.get_name(): Date,
    Datetime.get_name(): Datetime,
    ActiveURL.get_name(): ActiveURL,
    Filled.get_name(): Filled,
    Numberic.get_name(): Numberic,
    Digits.get_name(): Digits
}

