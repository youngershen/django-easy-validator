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

## Installation

install using pip :

`pip install django-easy-validator`

install using source code:

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

2. spawn your validation class then call validate method to get it out.

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
- [active_url](#active_url)
- [numberic](#numberic)
- [digits](#digits)
- [regex](#regex)
- [email](#email)

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

## Advanced Topic

advanced topic

