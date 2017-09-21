# PROJECT : validator
# TIME : 17-9-11 下午3:00
# AUTHOR : Younger Shen
# EMAIL : younger.x.shen@gmail.com
from copy import deepcopy
from django.utils.translation import ugettext as _


class BaseRule:
    name = 'baserule'
    message = _('i am the base rule')

    def __init__(self, name, value, *args, message=None):
        self.name = name
        self.value = value
        self.args = args
        self.status = True
        self.message = message if message else self.message

    def check(self):
        raise NotImplementedError

    def get_status(self):
        return self.status

    def get_message(self):
        return self.message


class Required(BaseRule):
    name = 'required'
    message = '{FIELD} is required'

    def check(self):
        self.status = not not self.value

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

    messages = {}
    info = {0: _('OK')}

    def __init__(self, data, request):
        self.data = deepcopy(data)
        self.request = request
        self.status = True
        self.code = 0
        self.__message__ = {}

    def validate(self):
        validation = self.__get_validation__()
        for item in validation:
            name = item.get('name', '')
            value = item.get('value', '')
            rules = item.get('rules', [])

            for rule in rules:
                rule_name = rule.get('name')
                params = rule.get('params')
                rule_class = RULES.get(rule_name)
                message = self.message.get(name, {}).get(rule_name, None)
                rule_instance = rule_class(name, value, *params, message=message)
                rule_instance.check()
                if not rule_instance.get_status():
                    self.status = False
                    self.set_message(name, rule_name, rule_instance.get_message())
        else:
            self.check() if self.status else ''
            return self.status, self.code, self.get_message(), self.get_info()

    def get(self, name, default=None):
        return self.data.get(name, default)

    def check(self):
        pass

    def get_info(self):
        info = self.info.get(self.code, '') if self.status else ''
        return info

    def get_message(self):
        return self.__message__

    def set_message(self, name, rule, message):
        if name not in self.__message__.keys():
            self.__message__.update({name: {}})
        self.__message__[name].update({rule: message})

    def __get_validation__(self):
        ret = []
        for name, validation in getattr(self, 'validation').items():
            rules = self.__get_rules__(validation)
            value = self.get(name)
            data = {'name': name, 'value': value, 'rules': list(rules)}
            ret.append(data)
        return ret

    def __get_rules__(self, validation):
        rules = map(self.__get_rule__, validation.split('|'))
        return rules

    @staticmethod
    def __get_rule__(rule):
        info = list(map(lambda s: s.strip(), rule.split(':')))
        name = info[0]
        params = map(lambda s: s.strip(), ''.join(info[1:]).split(','))
        rules = {'name': name, 'params': list(params)}
        return rules


RULES = {
    'required': Required
}
