# Django contrib validator
this piece of software is inspired by the validation system of [laravel](https://laravel.com/docs/5.5/validation), 
you can use this software to validate your POST/GET data easily and softly.

## Requirements

- Python 3.4
- Python 3.5
- Python 3.6

## Installation

install using pip :

`pip install django-contrib-validator`

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

## Advanced Topic

advanced topic

