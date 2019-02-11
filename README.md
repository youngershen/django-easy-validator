# Django Easy Validator
this piece of software is inspired by the validation system of [laravel](https://laravel.com/docs/5.5/validation), 
you can use this software to validate your POST/GET data easily and softly.

![Travis](https://img.shields.io/travis/youngershen/django-easy-validator.svg)
![codecov](https://codecov.io/gh/youngershen/django-easy-validator/branch/master/graph/badge.svg)
![PyPI - License](https://img.shields.io/pypi/l/django-easy-validator.svg)
![PyPI](https://img.shields.io/pypi/v/django-easy-validator.svg)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/django-easy-validator.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-easy-validator.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/youngershen/django-easy-validator.svg)


## Requirementse

- Python 3.4
- Python 3.5
- Python 3.6
- Python 3.7
- Django 1.6 +

## Installation

install from pypi :

`pip install django-easy-validator`

install from source code:

`python setup.py install`

## Usage

1. create your own validator with Validator class.

```python
    from validator import Validator
    
    class LoginValidator(Validator):
        username = 'required|email'
        password = 'required'
        
        message = {
            'username': {
                'required': _('username is required'),
                'email': _('username is not an email address')
            },
            'password': {
                'required': _('password is required')
            }
        }
        
```

2. spawn your validation class then call validate method to check it out.

```python
       
    validator = LoginValidator({'username': 'michael', 'password': '12345678'})
    status = validator.validate()
    if status:
        print("login succeed")
    else:
        errors = validator.get_message()
        print(errors)
```

## Supported Rules

- [required](#required)
- [accepted](#accepted)
- [date](#data)
- [date_before](#date_before)
- [date_after](#date_after)
- [date_range](#date_range)
- [datetime](#datetime)
- [datetime_before](#datetime_before)
- [datetime_after](#datetime_after)
- [datetime_range](#datetime_range)
- [active_url](#active_url)
- [numberic](#numberic)
- [digits](#digits)
- [regex](#regex)
- [email](#email)
- [min_length](#min_length)
- [max_length](#max_length)
- [ids](#ids)
- [cellphone](#cellphone)
- [alphabet](#alphabet)
- [switch](#switch)
- [unique](#unique)
- [size](#size)
- [min](#min)
- [max](#max)
- [file](#file)
- [image](#image)
- [video](#video)
- [audio](#audio)
- [attachement](#attachement)
- [alpha_dash](#alpha_dash)
- [alpha_number](#alpha_number)
- [array](#array)
- [date_before_equal](#date_before_equal)
- [date_after_equal](#date_after_equal)
- [datetime_before_equal](#datetime_before_equal)
- [datetime_after_equal](#datetime_after_equal)
- [between](#between)
- [boolean](#boolean)
- [username](#username)
- [password](#password)
- [ASCII](#ASCII)

--------------------------------------------------------------

### required

```python

    class LoginValidator(Validator):
        username = 'required'
```

the field with required rule cant be null or empty.

### accepted

```python
    class LoginValidator(Validator):
        username = 'required'
        remember_me = 'accepted'
```

the field with accepted must be one of the following strings, and the
string case is insensitive.

```python
    ['yes', 'no', 'true', 'false', '0', '1']
``` 

### date

```python
    class RegisterValidator(Validator):
        birthday = 'required|date:%Y-%m-%d'
```

the field with date must be a python date format string, the parameter 
should be a format suit the datetime.datetime.strptime function.

### date_before

```python
    class SubmitValidator(Validator):
        due = 'required|date_before:2017-12-31'
```

the field with date_before must be a date format string suit xxxx-mm-dd.

### date_after

```python
    class SubmitValidator(Validator):
        date = 'required|date_after:2017-11-12'
```
the field with date_after must be a date format string suit xxxx-mm-dd.

### date_range

```python
    class SubmitValidator(Validator):
        date_range = 'required|date_range:2017-01-01,2017-12-31'
```

the field with date_range must be 2 date format strings and it should suit xxxx-mm-dd.


### datetime

```python
    class RegisterValidator(Validator):
        login_time = 'required|datetime:%Y-%m-%d %H:%M:%S'
```

the field with datetime and the parameter must be a datetime string suit the datetime.datetime.strptime function.

### datetime_before
```python
    class LoginValidator(Validator):
        time = 'required|datetime_before:2017-12-12 13:14:00'
```

the field with datetime_before must be a datetime string can strap to a datetime object and so as the parameter.


### datetime_after

```python
    class LoginValidator(Validator):
        time = 'required|datetime_after:2017-12-12 13:14:00'
```

the field with datetime_after must be a datetime string can strap to a datetime object and so as the parameter.


### datetime_range

```python
    class LoginValidator(Validator):
        period = 'datetime_range:2017-12-12 13:14:00, 2017-12-15 13:14:00'

```

### active_url

```python
    class ActiveURLValidator(Validator):
        url = 'active_url'
```

the field with active_url must be a active url you could connect to and get reply.

### numberic

```python
    class RegisterValidator(Validator):
        id_number = 'required|numberic'
```

the field with numberic must be a number, it should be a integer not a float or something.

### digits

```python
    class RegisterValidator(Validator):
        product_series = 'required|digits'
```

the field with digits must only contains digits token.

### regex

```python
    class RegisterValidator(Validator):
        id_number = 'required|regex:^0[0-9]{5,10}$'
```

the field with regex must be a string, the parameter could be any regex pattern string, this
rule will match the field value with the paramter pattern out.

### email

```python
    class RegisterValidator(Validator):
        username = 'required|email'
        
```

the field with email must be a valid email address string.


### min_length

```python

class Register(Validator):
    password = 'min_length:8'

```

the field with **min_length** must has the minimal length of string or value of number.

### max_length

```python

class RegisterValidator(Validator):
    username = 'max_length:20'

```

the field with **min_length** must has the minimal length of string or value of number.


### ids

```python

class DeleteValidator(Validator):
    ids = 'ids'
```

the field with ids must be a integer string splited by the comma, such as '1,2,3,4,5'


### cellphone

```python

class RegisterValidator(Validator):
    phone = 'cellphone'

```

the field with cellphone rule must be a real cellphone number , it could be '+8613811754531' or just '13811754531'


### alphabet

```python

class RegisterValidator(Validator):
    name = 'alphabet'

```

the field with alphabet must be a standard alphabet string.


### switch

```python

class LoginValidator(Validator):
    rememberme ='switch:yes,no'

```

the field with switch must be in the params array, it this case , rememberme must be yes or no.


### unique

```python

class RegisterValidator(Validator):
    username = 'unique:AUTH_USER_MODEL,username'
    email = 'unique:account.User,email'

```

the field with unique must has 2 parameters , the first is appname.modelname, the second is the field to check,
actually it is also the column to check if is already exists in this table, if you want to validate the django auth
user, the first paramater must be AUTH_USER_MODEL.


### size
```python

class UpdateProfileValidator(Validator)
    avatar = 'image|size:2048'

```

the field with size has 4 kind of types , if the given field is an file, the parameter means the size of the file with KB,
if the field is a string , the parameter means the size is the string length, if the field is an integer , the size means
the integer value, if the field is an array, the size means the array size.


### min

```python

class UpdateProfileValidator(Validator):
    profile = 'image|min:2048'

```

the field with min has the same meaning of size, it's just check the minimal of the field , the size is check the equal of the field.

### max

```python

class UpdateProfileValidator(Validator):
    profile = 'image|min:2048'

```

the field with min has the same meaning of size, it's just check the maximal of the field , the size is check the equal of the field.


### file

```python

class UploadValidator(Validator):
    file = 'file:png,jpeg,zip,rar'

```

the field with file rule is to check the file type. parameters needed to be a string array.


### image

```python

class UploadValidator(Validator):
    file = 'image'

```

the field with file image rule just do the same thing like file , it is a convenient way to check the common image type , in this way you do not need to add image ext parameter.
the check type is ['png', 'jpeg', 'gif', 'jpg', 'svg'] .


### video

```python

class UploadValidator(Validator):
    file = 'video'

```

the field with video rule just do the same thing like file , it is a convenient way to check the common video type , in this way you do not need to add video ext parameter.
the check type is  ['mp4', 'avi', 'mkv', 'flv', 'rmvb'].


### audio

```python

class UploadValidator(Validator):
    file = 'audio'

```

the field with audio rule just do the same thing like file , it is a convenient way to check the common audio type , in this way you do not need to add video ext parameter.
the check type is  ['mp3', 'wma', 'flac', 'ape', 'ogg'].


### attachement

```python

class UploadValidator(Validator):
    file = 'attachement'
```

the field with attachement rule just do the same thing like file , it is a convenient way to check the common attachement type , in this way you do not need to add video ext parameter.
the check type is ['doc', 'zip', 'ppt', 'docx', 'excel', 'rar'].

### alpha_dash

```python
class RegisterValidator(Validator):
    username = 'alpha_dash'

```

the field with alpha_dash rule is just check out if the string only includes alphabet characters and dash character.


### alpha_number

```python
class RegisterValidator(Validator):
    username = 'alpha_number'

```
the field with alpha_number the given value must conbines with only alphabets and numbers.


### array

```python
class RegisterValidator(Validator):
    hobbies = 'array'

```

the field with array must be a array string ,such as 'guitar, computer, music, food'.

### date_before_equal

```python
class RegisterValidator(Validator):
    due_at = 'date_before_equal:2018-01-08'
```

the field with date_before_equal just check the given value must be a date string and before or equal the given parameter.

### date_after_equal

```python
class RegisterValidator(Validator):
    due_at = 'date_after_equal:2018-01-08'
```

the field with date_after_equal just check the given value must be a date string and afer or equal the given parameter.

### datetime_before_equal

```python
class RegisterValidator(Validator):
    due_at='datetime_before_equal:1990-12-12 06:08:26'
```

the field with datetime_before_equal just check the given value must be a datetime string and befor the given parameter.

### datetime_after_equal

```python
class RegisterValidator(Validator):
    due_at='datetime_after_equal:1990-12-12 06:08:26'
```

the field with datetime_after_equal just check the given value must be a datetime string and after the given parameter.


### between

```python
class RegisterValidator(Validator):
    age = 'between:10, 15'
```

the field with between requires the given field value must be a integer number and it's value must between the parameters.


### boolean

```python
class RegisterValidator(Valiadtor):
    remember = 'boolean'

```

the field with boolean requires the given value should be one of this '['0', '1', 'true', 'false']'

### username

```python
class RegisterValidator(Validator):
    username = 'username'
```

the field with username requires the given value starts with an alphabet character and it could includes with numbers , dash, underscore.

### password
```python
class RegisterValidator(Validator):    
    password = 'password:low'

```

the field with password ruls requires an parameter , it could be : low, middle , high. 
the 3 different check methods has different check level.

the low method means the password length must longer than 7

the middle method means the password length must longer than 7 and it sould contains lower , upper latin characters and digits

the high method means the password lenght must longer than 7 and it sould contains lower , upper latin characters and digits, and special

characters.

### ASCII
```python
class ASCIIValidator(Validator):
    ascii = 'ascii'

```

the ascii requires the given value only includes ascii characters.


### same

```python
class SameValidator(Validator):
    password = 'required|min_lengh:8'
    password_confirm = 'same:password'

```

the same rule just validate the give field vale checks the value if is same as the other value.

## Advanced Topic

### Custom Validation Rules

```python
# define the rule
from validator import BaseRule
class TestRule(BaseRule):
    name = 'test_rule'
    message = 'test custom rule failed'
    description = 'just for custom rule test'

    def check_value(self):
        self.status = True if self.field_value == 'test' else False

    def check_null(self):
        pass


# define a validator to use the rule
class TestRuleValidator(Validator):
    name = 'test_rule'

# to run the validation
extra_rules = { TestRule.get_name(): TestRule }
validator = TestRuleValidator(extra_rules=extra_rules, data={'name': 'test'})
assert validator.validate()

```

custom a validation rule is very easy, you just import the BaseRule and implements the method ,
the most important thing is before you use your rule , you should pass it to your validator 
class when it init through the extra_rules parameter.
