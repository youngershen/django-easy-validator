# PROJECT : django-easy-validator
# TIME    : 18-1-2 上午9:44
# AUTHOR : Younger Shen
# EMAIL : younger.x.shen@gmail.com
# CELL : 13811754531
# WECHAT : 13811754531
# https://github.com/youngershen/

import re
import socket
import datetime
from copy import deepcopy

try:
    # django not installed
    from django import utils
except ImportError:
    def _(text):
        return text
else:
    try:
        # django not configured
        from django.core.exceptions import ImproperlyConfigured
        from django.utils.translation import gettext_lazy as _
    except ImproperlyConfigured:
        def _(text):
            return text


class RuleNotFoundError(Exception):
    message = _('{NAME} rule not found !!!')

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.message.format(NAME=self.name)


class RuleMissedParameterError(Exception):
    pass


class InvalidRuleParamterError(Exception):
    pass


class BaseRule:
    name = 'base_rule'
    message = _('{VALUE} of {FIELD} field is match rule {RULE_NAME}.')
    description = _('describe the propuse of the current rule.')
    parse_args = True

    def __init__(self, field_name, field_value, args, data=None, message=None):
        self.field_name = field_name
        self.field_value = field_value
        self.args = list(map(lambda d: d.strip(), args.split(','))) if self.parse_args else args
        self.status = True
        self.message = message if message else self.message
        self.data = data

    def check(self):
        if self.field_value:
            self.check_value()
        else:
            self.check_null()

    def check_value(self):
        raise NotImplementedError()

    def check_null(self):
        raise NotImplementedError()

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
    description = _('check if the value is in the params array.')

    def check_value(self):
        self.status = self.field_value in self._get_params()

    def check_null(self):
        pass

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
    description = _('The field under validation must be entirely alphabetic characters.')

    def check_null(self):
        pass

    def check_value(self):
        self.status = True if re.match(self.regex, self.field_value) else False


class MinLength(BaseRule):
    name = 'min_length'
    message = _('{VALUE} of {FIELD} is shotter than {MIN}')
    description = _('check the field as a string and test the length if suites the given number')

    def check_null(self):
        pass

    def check_value(self):
        self.status = len(str(self.field_value)) >= int(self.args[0])

    def get_message(self):
        return self.message.format(VALUE=self.field_value, FIELD=self.field_name, MIN=self.args[0])


class MaxLength(BaseRule):
    name = 'max_length'
    message = _('{VALUE} of {FIELD} is longger than {MAX}')
    description = _('check the field as a string and test the length if suites the given number')

    def check_null(self):
        pass

    def check_value(self):
        self.status = len(str(self.field_value)) <= int(self.args[0])

    def get_message(self):
        return self.message.format(VALUE=self.field_value, FIELD=self.field_name, MAX=self.args[0])


class IDS(BaseRule):
    name = 'ids'
    message = _('{VALUE} of {FIELD} is not a id series')
    description = _('check it the given value is id string such as 1,2,3,4')
    regex = r'^\d+(?:,\d+)*$'

    def check_null(self):
        pass

    def check_value(self):
        self.status = True if re.match(self.regex, self.field_value) else False


class Cellphone(BaseRule):
    name = 'cellphone'
    regex = r'^([\+]?[0-9]{2})?1[0-9]{10}$'
    message = _('{VALUE} of {FIELD} is not a cellphone number')
    description = _('check if the given value is a cellphone number , '
                    'if there is a internation code it sould begin with + .')

    def check_null(self):
        pass

    def check_value(self):
        self.status = True if re.match(self.regex, self.field_value) else False


class Regex(BaseRule):
    name = 'regex'
    message = _('{VALUE} of {FIELD} is not mathc the pattern {REGEX}')
    description = _('check the given value if suits the regex')
    parse_args = False

    def check_null(self):
        pass

    def check_value(self):
        self.status = True if self._match() else False

    def get_message(self):
        return self.message.format(VALUE=self.field_value, FIELD=self.field_name, REGEX=self._get_regex())

    def _get_regex(self):
        return self.args

    def _match(self):
        return re.match(self._get_regex(), self.field_value)


class Email(BaseRule):
    name = 'email'
    message = _('{VALUE} of {FIELD} is not an email address')
    description = _('check for email addresses')
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    def check_null(self):
        pass

    def check_value(self):
        self.status = True if re.match(self.pattern, self.field_value) else False


class Digits(BaseRule):
    name = 'digits'
    message = _('{VALUE} of {FIELD} is not match digits')
    description = _('check if the given value is made of digits')

    def check_null(self):
        pass

    def check_value(self):
        digits_regex = r'[0-9]+'
        self.status = True if re.fullmatch(digits_regex, str(self.field_value)) else False


class Numberic(BaseRule):
    name = 'numberic'
    message = _('{VALUE} of {FIELD} is not match numberic')
    description = _('check if the given value is a integer number')

    def check_null(self):
        pass

    def check_value(self):
        regex = r'^[1-9]{1}[0-9]*'
        self.status = True if re.fullmatch(regex, str(self.field_value)) else False


class ActiveURL(BaseRule):
    name = 'active_url'
    message = '{VALUE} of {FIELD} field is not a active URL'
    description = _('check if the given value if an active url you can visit.')

    def check_null(self):
        pass

    def check_value(self):
        try:
            socket.gethostbyname(self.field_value)
        except socket.gaierror:
            self.status = False


class Date(BaseRule):
    name = 'date'
    message = _('{VALUE} of {FIELD} field is not a valid date format as {FORMAT_STR}')
    format_str = '%Y-%m-%d'
    description = _('check the given value if suits the date format of format_str')

    def get_format(self):
        return self.args[0] if 1 == len(self.args) and self.args[0] else self.format_str

    def check_null(self):
        pass

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
    description = _('check the given value if suits the date time format of format_str')

    def get_format(self):
        return self.args[0] if 1 == len(self.args) and self.args[0] else self.format_str

    def check_null(self):
        pass

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
    description = _('check the given value if before the date time format of format_str')

    def check_null(self):
        pass

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
    description = _('check the given value if after the date time format of format_str')

    def check_null(self):
        pass

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
    description = _('check the given value if between the param date string')

    def check_null(self):
        pass

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
    description = _('check the given value if before the datetime format of format_str')

    def check_null(self):
        pass

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
    description = _('check the given value if between the datetime format of the param datetime')

    def check_null(self):
        pass

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
    description = _('check the given value if after the datetime format of format_str')

    def check_null(self):
        pass

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


# FIX: thie required should filter the space in the given value
class Required(BaseRule):
    name = 'required'
    message = _('{FIELD} field is required')
    description = _('the given field is required')

    def check_null(self):
        self.status = False

    def check_value(self):
        pass


class Accepted(BaseRule):
    name = 'accepted'
    message = _('{VALUE} of {FIELD} field must in which of : {FLAGS}')
    flag = ['yes', 'no', 'true', 'false', '0', '1']
    description = _('the given field must in the flag array')

    def get_flag_str(self):
        return ', '.join(self.flag)

    def check_null(self):
        pass

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
    message = _('{VALUE} of {MODEL} with {MODEL_FIELD} is not unique')
    description = _('the given value must unique of the table')

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


class AlphaDash(BaseRule):
    name = 'alpha_dash'
    message = _('{VALUE} is invalid alpha dash format string.')
    regex = '[a-zA-Z-_]+'
    description = _('The field under validation may have alpha-numeric characters, as well as dashes and underscores.')

    def check_value(self):
        self.status = re.match(self.regex, self.field_value)

    def check_null(self):
        pass


class AlphaNumber(BaseRule):
    name = 'alpha_number'
    message = _('{VALUE} is not a alpha-number string.')
    regex = '[a-zA-Z0-9]+'
    description = _('the given value must conbines with only alphabets and numbers ')

    def check_value(self):
        self.status = re.match(self.regex, self.field_value)

    def check_null(self):
        pass


class Array(BaseRule):
    name = 'array'
    message = _('{VALUE} is not a comma splited string')
    description = _('the given must be a comma splited string.')

    def check_value(self):
        self.status = True if len(self.field_value.split(',')) > 2 else False

    def check_null(self):
        pass


class DateBeforeEqual(BaseRule):
    name = 'date_before_equal'
    message = _('{VALUE} of {FIELD} is not before or equal date {DATE}')
    field_format_str = '%Y-%m-%d'
    param_format_str = '%Y-%m-%d'
    description = _('check the given value if before or equal the date time format of format_str')

    def check_null(self):
        pass

    def check_value(self):
        param_date = self._get_param_date()
        field_date = self._get_field_date()
        self.status = field_date <= param_date

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


class DateAfterEqual(BaseRule):
    name = 'date_after_equal'
    message = _('{VALUE} of {FIELD} is not after or equal date {DATE}')
    field_format_str = '%Y-%m-%d'
    param_format_str = '%Y-%m-%d'
    description = _('check the given value if after or equal the date time format of format_str')

    def check_null(self):
        pass

    def check_value(self):
        param_date = self._get_param_date()
        field_date = self._get_field_date()
        self.status = field_date >= param_date

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


class DateTimeBeforeEqual(BaseRule):
    name = 'datetime_before_equal'
    message = _('{VALUE} of {FIELD} is not before or equal {DATETIME}')
    field_format_str = '%Y-%m-%d %H:%M:%S'
    param_format_str = '%Y-%m-%d %H:%M:%S'
    description = _('check the given value if before or equal the datetime format of format_str')

    def check_null(self):
        pass

    def check_value(self):
        field_datetime = self._get_field_datetime()
        param_datetime = self._get_param_datetime()
        self.status = field_datetime <= param_datetime

    def get_message(self):
        return self.message.format(VALUE=self.field_value, FIELD=self.field_name, DATETIME=self.args[0])

    def _get_field_datetime(self):
        return datetime.datetime.strptime(self.field_value, self.field_format_str)

    def _get_param_datetime(self):
        datetime_str = self.args[0] if len(self.args) == 1 else None
        return datetime.datetime.strptime(datetime_str, self.param_format_str)


class DatetimeAfterEqual(BaseRule):
    name = 'datetime_after_equal'
    message = _('{VALUE} of {FIELD} is not after or equal {DATETIME}')
    field_format_str = '%Y-%m-%d %H:%M:%S'
    param_format_str = '%Y-%m-%d %H:%M:%S'
    description = _('check the given value if after or equal the datetime format of format_str')

    def check_null(self):
        pass

    def check_value(self):
        field_datetime = self._get_field_datetime()
        param_datetime = self._get_param_datetime()
        self.status = field_datetime >= param_datetime

    def get_message(self):
        return self.message.format(VALUE=self.field_value, FIELD=self.field_name, DATETIME=self.args[0])

    def _get_field_datetime(self):
        return datetime.datetime.strptime(self.field_value, self.field_format_str)

    def _get_param_datetime(self):
        datetime_str = self.args[0] if len(self.args) == 1 else None
        return datetime.datetime.strptime(datetime_str, self.param_format_str)


class Between(BaseRule):
    name = 'between'
    message = _('{VALUE} is not between of the {START} -> {END}')
    description = _('check the given value if between the params, it\'s only adapted for integer and string value')

    def check_value(self):
        start, stop = self._get_params()
        length = self.get_value_length()
        self.status = start <= length <= stop

    def get_value_length(self):
        try:
            length = int(self.field_value)
        except ValueError:
            length = len(self.field_value)

        return length

    def check_null(self):
        pass

    def get_message(self):
        start, stop = self._get_params()
        start, stop = stop, start if start > stop else None
        return self.message.format(VALUE=self.field_value, START=start, STOP=stop)

    def _get_params(self):
        if len(self.args) < 2:
            raise InvalidRuleParamterError(_('between rule needs 2 params.'))

        else:
            start = int(self.args[0])
            stop = int(self.args[1])
            return start, stop


class Boolean(BaseRule):
    name = 'boolean'
    message = _('{VALUE} can not covert to boolean type')
    description = _('check the given value if boolean type')
    type_ = ['0', '1', 'true', 'false']

    def check_value(self):
        self.status = True if self.field_value.strip().lower() in self.type_ else False

    def check_null(self):
        pass


class FileRuleMixin:
    def check_value(self):
        self._check_file()

    def check_null(self):
        pass

    def _check_file(self):
        ext = self._get_ext()
        exts = self._get_exts()
        self.status = ext in exts

    def _check_ext(self):
        ext = self._get_ext()
        exts = self._get_exts()
        return ext in exts

    def _get_ext(self):
        name = self.field_value.name
        ext = name.split('.')[-1]
        return ext

    def _get_exts(self):
        return self.exts

    def get_message(self):
        file_name = self.field_value.name
        return self.message.format(FILE_NAME=file_name)


class File(FileRuleMixin, BaseRule):
    name = 'file'
    message = _('{FILE_NAME} is not allowed to upload')
    description = _('check the uploaded file ext if allowed to upload this kind of file. ')

    def _get_exts(self):
        return self.args


class Image(File):
    name = 'image'
    exts = ['png', 'jpeg', 'gif', 'jpg', 'svg']


class Video(File):
    name = 'video'
    exts = ['mp4', 'avi', 'mkv', 'flv', 'rmvb']


class Audio(File):
    name = 'audio'
    exts = ['mp3', 'wma', 'flac', 'ape', 'ogg']


class Attachement(File):
    name = 'attachement'
    exts = ['doc', 'zip', 'ppt', 'docx', 'excel', 'rar']


class SizeMixin:
    types = ['string', 'number', 'array', 'file']

    def check_value(self):
        _type = self.get_arg(0)
        _size = self.get_arg(1)

        if _type and _size and _type in self.types:
            size = self._get_field_size(_type)
            self._check_size(float(_size), float(size))
        else:
            raise InvalidRuleParamterError(_('invalid rule paramters'))

    def check_null(self):
        pass

    def _check_size(self, *args, **kwargs):
        raise NotImplementedError()

    def _get_field_size(self, _type):
        if 'string' == _type:
            return self._get_str_size()

        if 'number' == _type:
            return self._get_number_size()

        if 'array' == _type:
            return self._get_array_size()

        if 'file' == _type:
            return self._get_file_size()

        raise InvalidRuleParamterError(_('invalid rule parameters'))

    def _get_str_size(self):
        _value = str(self.field_value)
        return len(_value)

    def _get_number_size(self):
        _value = float(self.field_value)
        return _value

    def _get_file_size(self):
        size = self.field_value.size
        return size / 1000

    def _get_array_size(self):
        _value = len(self.field_value.split(','))
        return _value

    def get_message(self):
        _type = self.get_arg(0)
        size = self._get_field_size(_type)
        return self.message.format(FIELD=self.field_name, SIZE=size)


class Min(SizeMixin, BaseRule):
    name = 'min'
    message = _('size of {FIELD} is larger than {SIZE}')
    description = _('')

    def _check_size(self, _size, size):
        self.status = _size <= size


class Max(SizeMixin, BaseRule):
    name = 'max'
    message = _('size of {FIELD} is smaller than {SIZE}')
    description = _('')

    def _check_size(self, _size, size):
        self.status = _size >= size


class Size(SizeMixin, BaseRule):
    name = 'size'
    message = _('size of {FIELD} is not equals to {SIZE}')
    description = _('The field under validation must have a size matching the given value. '
                    'For string data, value corresponds to the number of characters. '
                    'For numeric data, value corresponds to a given integer value. '
                    'For an array, size corresponds to the count of the array. '
                    'For files, size corresponds to the file size in kilobytes.')

    def _check_size(self, _size, size):
        self.status = _size == size


class Username(BaseRule):
    name = 'username'
    message = _('the input {VALUE} is not a proper username.')
    description = _('this rule will check the normal username, the initial of username must be a alphabet character and'
                    'it could conbimes with digits, dot, underscore and dash.')

    regex = r'^[a-z]{1}[a-z0-9\.\-_]*$'

    def check_value(self):
        self.status = True if re.fullmatch(self.regex, self.field_value) else False

    def check_null(self):
        pass


class Password(BaseRule):
    name = 'password'
    message = _('the input is not a proper password.')
    description = _('a simple password validate rule , it has 3 level strength rule for password,'
                    'the simple rule just needs the password length has more than 7 simple '
                    'characters includes digits number and alphabet characters'
                    'the middle rule needs the password has UPPER case characters , '
                    'lower case characters, and digits numbers'
                    'the high rule needs the password combines with special '
                    'characters, and UPPER case'
                    'characters and lowe case chracters, and digits numbers.')

    digits = 48, 57
    latin_upper = 65, 96
    latin_lower = 97, 122
    special = (33, 47), (58, 64), (123, 126)

    level = ['low', 'middle', 'high']

    def check_value(self):
        level = self.get_level()
        if 'low' == level:
            self.status = self.check_low()
        elif 'middle' == level:
            self.status = self.check_middle()
        elif 'high' == level:
            self.status = self.check_high()

    def check_null(self):
        pass

    def get_level(self):
        level = self.args[0]
        if level not in self.level:
            raise InvalidRuleParamterError('parameters must be one of : low, middle, high')
        else:
            return level

    def check_low(self):
        return len(self.field_value) >= 7

    def check_middle(self):
        return len(self.field_value) >= 7 and \
               self.check_latin_lower() and \
               self.check_latin_upper() and \
               self.check_digits()

    def check_high(self):
        return len(self.field_value) >= 7 and \
               self.check_latin_lower() and \
               self.check_latin_lower() and \
               self.check_digits() and \
               self.check_special()

    def check_digits(self, number=1):
        seq = self.parse_value()
        count = 0
        for c in seq:
            if self.digits[0] <= c <= self.digits[1]:
                count = count + 1

        return count >= number

    def check_latin_lower(self, number=1):
        seq = self.parse_value()
        count = 0
        for c in seq:
            if self.latin_lower[0] <= c <= self.latin_lower[1]:
                count = count + 1
        return count >= number

    def check_latin_upper(self, number=1):
        seq = self.parse_value()
        count = 0
        for c in seq:
            if self.latin_upper[0] <= c <= self.latin_upper[1]:
                count = count + 1
        return count >= number

    def check_special(self, number=1):
        seq = self.parse_value()
        count = 0
        for c in seq:
            if self.special[0][0] <= c <= self.special[0][1] or \
                    self.special[1][0] <= c <= self.special[1][1] or \
                    self.special[2][0] <= c <= self.special[2][1]:
                count = count + 1
        return count >= number

    def parse_value(self):
        ret = map(lambda d: ord(d), ','.join(self.field_value).split(','))
        return list(ret)


class ASCII(BaseRule):
    name = 'ascii'
    message = _('the input {VALUE} value is not a proper ASCII character.')
    description = _('check the given value if is a ascii character series.')

    def check_value(self):
        self.status = self.check_ascii()

    def check_null(self):
        pass

    def check_ascii(self):
        seq = filter(lambda d: ord(d) > 127, ','.join(self.field_value).split(','))
        return False if list(seq) else True


class PrintableASCII(BaseRule):
    name = 'pascii'
    message = _('this input {VALUE} is not a proper printable ASCII character string.')
    description = _('check the give string if it is a printable ASCII string only'
                    'contains the characters from 32 to 255')

    def check_value(self):
        no_blank = self.get_arg(0)
        if no_blank:
            self.status = self.check_string_no_blank()
        else:
            self.status = self.check_string()

    def check_null(self):
        self.status = False

    def check_string(self):
        if not self.field_value:
            return False

        seq = filter(lambda d: ord(d) > 255, ','.join(self.field_value).split(','))
        return False if list(seq) else True

    def check_string_no_blank(self):
        code_list = [
            *list(range(33, 126)),
            128,
            *list(range(130, 140)),
            142,
            *list(range(142, 156)),
            *list(range(158, 159)),
            *list(range(161, 172)),
            *list(range(174, 255))]

        field_value = self.field_value.strip()

        if not field_value:
            return False
        else:
            for ch in field_value:
                if ord(ch) not in code_list:
                    return False
            else:
                return True


class Same(BaseRule):
    name = 'same'
    message = _('the input value is not same as the value of {PARAM_FIELD}')
    description = _('')

    def check(self):
        name = self.get_arg(0)
        if name:
            value = self.data.get(name, None)
            self.status = str(value) == str(self.field_value)
        else:
            raise InvalidRuleParamterError(_('wrong paramter for the Same Rule.'))

    def check_null(self):
        self.status = self.check()

    def check_value(self):
        self.status = self.check()

    def get_message(self):
        return self.message.format(FIELD=self.field_name,
                                   VALUE=self.field_value,
                                   RULE_NAME=self.name,
                                   PARAM_FIELD=self.get_arg(0),
                                   PARAM_VALUE=self.data.get(self.get_arg(0), None))


class Decimal(BaseRule):
    name = 'decimal'
    message = _('the input value {VALUE} of {FIELD} is not a decimal format number')
    description = _('')

    def check(self):
        self.status = self.check_decimal()

    def check_decimal(self):
        r = r'^[0-9]+(\.[0-9]+)?$'
        m = re.fullmatch(r, str(self.field_value))

        return True if m else False

    def check_null(self):
        self.check()

    def check_value(self):
        self.check()

    def get_message(self):
        return self.message.format(FIELD=self.field_name,
                                   VALUE=self.field_value)


class Exist(Unique):
    name = 'exist'
    message = _('{VALUE} of {MODEL} with {MODEL_FIELD}  not existis in database')
    description = _('the given value must exist in the table of the database')

    def check_model(self):
        model_name, model_field = self.args
        model = self.get_model(model_name)
        qs = model.objects.filter(**{model_field: self.field_value})
        return qs.exists()


class UniqueAgainst(Unique):
    name = 'unique_against'
    message = _('the given {MODEL_NAME} record is exist against '
                'the {MODEL_FIELD} column by {MODEL_VALUE} with value {VALUE}')
    description = _('check the given record weather exists in the database against the given column value')

    def check_model(self):
        model_name, model_field, model_value = self.args
        model = self.get_model(model_name)
        qs = model.objects.filter(**{model_field: self.field_value}).exclude(**{model_field: model_value})
        return not qs.exists()

    def get_message(self):
        return self.message.format(MODEL_NAME=self.args[0],
                                   MODEL_FIELD=self.args[1],
                                   MODEL_VALUE=self.args[2],
                                   VALUE=self.field_value)


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
        instance = rule_class(name, value, params, data=self.data, message=message)
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
        info = list(map(lambda s: s.strip(), rule.split(':', 1)))
        name = info[0]
        params = info[1] if len(info) == 2 else ''
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
    Unique.get_name(): Unique,
    Size.get_name(): Size,
    Min.get_name(): Min,
    Max.get_name(): Max,
    File.get_name(): File,
    Image.get_name(): Image,
    Video.get_name(): Video,
    Audio.get_name(): Audio,
    Attachement.get_name(): Attachement,
    AlphaDash.get_name(): AlphaDash,
    AlphaNumber.get_name(): AlphaNumber,
    Array.get_name(): Array,
    DateBeforeEqual.get_name(): DateBeforeEqual,
    DateAfterEqual.get_name(): DateAfterEqual,
    DateTimeBeforeEqual.get_name(): DateTimeBeforeEqual,
    DatetimeAfterEqual.get_name(): DatetimeAfterEqual,
    Between.get_name(): Between,
    Boolean.get_name(): Boolean,
    Username.get_name(): Username,
    Password.get_name(): Password,
    ASCII.get_name(): ASCII,
    Same.get_name(): Same,
    Decimal.get_name(): Decimal,
    Exist.get_name(): Exist,
    UniqueAgainst.get_name(): UniqueAgainst,
    PrintableASCII.get_name(): PrintableASCII
}
