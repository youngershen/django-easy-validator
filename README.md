# Django contrib validator
this software inspired by the validation system of [laravel](https://laravel.com/docs/5.5/validation), 
you can use this software to validate your data easily and softly.

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

### required

```python

    class LoginValidator(Validator):
        username = 'required'
```

the field with required rule cant be null or empty.

### accepted

### date

### date_before

### date_after

### date_range

## Advanced Topic

## advanced topic

