# PROJECT : django-easy-validator
# TIME    : 18-1-2 上午9:44
# AUTHOR  : 申延刚 <Younger Shen>
# EMAIL   : younger.shen@hotmail.com
# PHONE   : 13811754531
# WECHAT  : 13811754531
# WEBSITE : www.punkcoder.cn

import re
import socket
import datetime
from copy import deepcopy
from django.utils.translation import ugettext_lazy as _


class RuleNotFoundError(Exception):
    message = _('{NAME} rule not found !!!')

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.message.format(NAME=self.name)


class RuleMissedParameterError(Exception):
    pass


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

    def get_arg(self, index):
        if len(self.args) > index:
            return self.args[index]
        else:
            return None

    @classmethod
    def get_name(cls):
        return cls.name


class Switch(BaseRule):
    name = 'switch'
    message = _('{VALUE} of {FIELD} is not in [{SWITCH}]')

    def check_value(self):
        self.status = self.field_value in self._get_params()

    def get_message(self):
        switch_str = ','.join(self._get_params())
        return self.message.format(VALUE=self.field_value,
                                   FIELD=self.field_name,
                                   SWITCH=switch_str)

    def _get_params(self):
        return self.args if self.args else []


class Alphabet(BaseRule):
    name = 'alphabet'
    regex = r'[a-zA-Z]+'
    message = _('{VALUE} of {FIELD} is not alphabet')

    def check_value(self):
        self.status = True if re.match(self.regex, self.field_value) else False


class MinLength(BaseRule):
    name = 'min_length'
    message = _('{VALUE} of {FIELD} is shotter than {MIN}')

    def check_value(self):
        self.status = len(self.field_value) >= int(self.args[0])

    def get_message(self):
        return self.message.format(VALUE=self.field_value, FIELD=self.field_name, MIN=self.args[0])


class MaxLength(BaseRule):
    name = 'max_length'
    message = _('{VALUE} of {FIELD} is longger than {MAX}')

    def check_value(self):
        self.status = len(self.field_value) <= int(self.args[0])

    def get_message(self):
        return self.message.format(VALUE=self.field_value, FIELD=self.field_name, MAX=self.args[0])


class IDS(BaseRule):
    name = 'ids'
    message = _('{VALUE} of {FIELD} is not a id series')
    regex = r'^([0-9]+,)+[0-9]+$'

    def check_value(self):
        self.status = True if re.match(self.regex, self.field_value) else False


class Cellphone(BaseRule):
    name = 'cellphone'
    regex = r'^([\+]?[0-9]{2})?1[0-9]{10}$'
    message = _('{VALUE} of {FIELD} is not a cellphone number')

    def check_value(self):
        self.status = True if re.match(self.regex, self.field_value) else False


class Regex(BaseRule):
    name = 'regex'
    message = _('{VALUE} of {FIELD} is not mathc the pattern {REGEX}')

    def check_value(self):
        self.status = True if self._match() else False

    def get_message(self):
        return self.message.format(VALUE=self.field_value, FIELD=self.field_name, REGEX=self._get_regex())

    def _get_regex(self):
        return self.args[0] if len(self.args) == 1 else None

    def _match(self):
        return re.match(self._get_regex(), self.field_value)


class Email(BaseRule):
    name = 'email'
    message = _('{VALUE} of {FIELD} is not an email address')
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    def check_value(self):
        self.status = True if re.match(self.pattern, self.field_value) else False


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
        int(str(self.field_value))
        regex = r'^[1-9]{1}[0-9]*'
        self.status = True if re.match(regex, str(self.field_value)) else False


class ActiveURL(BaseRule):
    name = 'active_url'
    message = '{VALUE} of {FIELD} field is not a active URL'

    def check_value(self):
        try:
            socket.gethostbyname(self.field_value)
        except socket.gaierror:
            self.status = False


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
        self.status = field_date < param_date

    def _get_param_date(self):
        date_str = self.get_arg(0)

        if not date_str:
            raise RuleMissedParameterError(_('DateBefore Rule missed a paramter'))

        param_format_str = self.get_arg(1) if self.get_arg(1) else self.param_format_str
        date = datetime.datetime.strptime(date_str, param_format_str)
        return date

    def _get_field_date(self):
        field_format_str = self.get_arg(2) if self.get_arg(2) else self.field_format_str
        date = datetime.datetime.strptime(self.field_value, field_format_str)
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
        self.status = field_date > param_date

    def _get_param_date(self):
        date_str = self.args[0]

        if not date_str:
            raise RuleMissedParameterError('date_after missed a parameter')

        param_format_str = self.get_arg(1) if self.get_arg(1) else self.param_format_str
        date = datetime.datetime.strptime(date_str, param_format_str)
        return date

    def _get_field_date(self):
        field_format_str = self.get_arg(2) if self.get_arg(2) else self.field_format_str
        date = datetime.datetime.strptime(self.field_value, field_format_str)
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
        self.status = begin < date < end

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


class DatetimeBefore(BaseRule):
    name = 'datetime_before'
    message = _('{VALUE} of {FIELD} is not before {DATETIME}')
    field_format_str = '%Y-%m-%d %H:%M:%S'
    param_format_str = '%Y-%m-%d %H:%M:%S'

    def check_value(self):
        field_datetime = self._get_field_datetime()
        param_datetime = self._get_param_datetime()
        self.status = field_datetime < param_datetime

    def get_message(self):
        return self.message.format(VALUE=self.field_value, FIELD=self.field_name, DATETIME=self.args[0])

    def _get_field_datetime(self):
        return datetime.datetime.strptime(self.field_value, self.field_format_str)

    def _get_param_datetime(self):
        datetime_str = self.args[0] if len(self.args) == 1 else None
        return datetime.datetime.strptime(datetime_str, self.param_format_str)


class DatetimeRange(BaseRule):
    name = 'datetime_range'
    message = _('{VALUE} of {FIELD} is not in range of {BEGIN} to {END}')
    field_format_str = '%Y-%m-%d %H:%M:%S'
    param_format_str = '%Y-%m-%d %H:%M:%S'

    def check_value(self):
        field_datetime = self._get_field_datetime()
        begin, end = self._get_param_datetime()
        self.status = end > field_datetime > begin

    def get_message(self):
        return self.message.format(VALUE=self.field_value, FIELD=self.field_name, BEGIN=self.args[0], END=self.args[1])

    def _get_field_datetime(self):
        return datetime.datetime.strptime(self.field_value, self.field_format_str)

    def _get_param_datetime(self):
        begin_datetime_str = self.args[0] if len(self.args) == 2 else None
        begin = datetime.datetime.strptime(begin_datetime_str, self.param_format_str)

        end_datetime_str = self.args[1] if len(self.args) == 2 else None
        end = datetime.datetime.strptime(end_datetime_str, self.param_format_str)

        return begin, end


class DatetimeAfter(BaseRule):
    name = 'datetime_after'
    message = _('{VALUE} of {FIELD} is not in after {DATETIME}')
    field_format_str = '%Y-%m-%d %H:%M:%S'
    param_format_str = '%Y-%m-%d %H:%M:%S'

    def check_value(self):
        field_datetime = self._get_field_datetime()
        param_datetime = self._get_param_datetime()
        self.status = field_datetime > param_datetime

    def get_message(self):
        return self.message.format(VALUE=self.field_value, FIELD=self.field_name, DATETIME=self.args[0])

    def _get_field_datetime(self):
        return datetime.datetime.strptime(self.field_value, self.field_format_str)

    def _get_param_datetime(self):
        datetime_str = self.args[0] if len(self.args) == 1 else None
        return datetime.datetime.strptime(datetime_str, self.param_format_str)


class Required(BaseRule):
    name = 'required'
    message = '{FIELD} field is required'

    def check_null(self):
        self.status = False


class Accepted(BaseRule):
    name = 'accepted'
    message = '{VALUE} of {FIELD} field must in which of : {FLAGS}'
    flag = ['yes', 'no', 'true', 'false', '0', '1']

    def get_flag_str(self):
        return ', '.join(self.flag)

    def check_value(self):
        self.status = self.check_flag()

    def check_flag(self):
        flag = self.field_value.lower()
        return flag in self.flag or flag in list(self.args)

    def get_message(self):
        return self.message.format(FIELD=self.field_name,
                                   VALUE=self.field_value,
                                   FLAGS=self.get_flag_str(),
                                   RULE_NAME=self.name)


class Unique(BaseRule):
    name = 'unique'
    message = '{VALUE} of {MODEL} with {MODEL_FIELD} is not unique'

    def check_null(self):
        pass

    def check_value(self):
        self.status = self.check_model()

    def check_model(self):
        model_name, model_field = self.args
        model = self.get_model(model_name)
        qs = model.objects.filter(**{model_field: self.field_value})
        return not qs.exists()

    @staticmethod
    def get_model(name):
        from django.conf import settings
        from django.apps import apps

        if 'AUTH_USER_MODEL' == name:
            app, name = settings.AUTH_USER_MODEL.split('.')
        else:
            app, name = name.split('.')
        return apps.get_model(app, name)

    def get_message(self):
        return self.message.format(VALUE=self.field_value, FIELD=self.field_name,
                                   MODEL=self.args[0],
                                   MODEL_FIELD=self.args[1])


class MetaValidator(type):
    def __new__(mcs, *args, **kwargs):
        name, base, attrs = args
        attrs.update({'validation': mcs.get_attrs(attrs)})
        return super().__new__(mcs, *args)

    @staticmethod
    def get_attrs(attrs):
        return dict((k, v) for k, v in attrs.items() if not k.startswith('__') and isinstance(v, str))


class Validator(metaclass=MetaValidator):
    parse_args = True

    def __init__(self, data, request=None, extra_rules=None):
        self.data = deepcopy(data)
        self.request = request
        self.extra_rules = extra_rules
        self.status = True
        self.validate_message = {}
        self.validate_message_plain = {}

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

    def get_message_plain(self):
        return self.validate_message_plain

    def set_message(self, name, rule, message):
        self.validate_message.update({name: {}}) if name not in self.validate_message.keys() else None
        self.validate_message[name].update({rule: message})

        self.validate_message_plain.update({name: []}) if name not in self.validate_message_plain.keys() else None
        self.validate_message_plain[name].append(message)

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

    def _get_rule_info(self, rule):
        info = list(map(lambda s: s.strip(), rule.split(':', 1)))
        name = info[0]
        if self.parse_args:
            params = list(map(lambda s: s.strip(), ''.join(info[1:]).split(',')))
        else:
            params = list(map(lambda s: s.strip(), info[1:]))

        params = params if len(params) > 0 and params[0] is not None else ()

        rules = {'name': name, 'params': params}
        return rules


default_rules = {
    Required.get_name(): Required,
    Accepted.get_name(): Accepted,
    Date.get_name(): Date,
    DateBefore.get_name(): DateBefore,
    DateAfter.get_name(): DateAfter,
    DateRange.get_name(): DateRange,
    Datetime.get_name(): Datetime,
    DatetimeBefore.get_name(): DatetimeBefore,
    DatetimeAfter.get_name(): DatetimeAfter,
    DatetimeRange.get_name(): DatetimeRange,
    ActiveURL.get_name(): ActiveURL,
    Numberic.get_name(): Numberic,
    Digits.get_name(): Digits,
    Regex.get_name(): Regex,
    Email.get_name(): Email,
    MinLength.get_name(): MinLength,
    MaxLength.get_name(): MaxLength,
    IDS.get_name(): IDS,
    Cellphone.get_name(): Cellphone,
    Alphabet.get_name(): Alphabet,
    Switch.get_name(): Switch,
    Unique.get_name(): Unique
}
