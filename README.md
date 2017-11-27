# django contrib validator
this software inspired by the validation system of [laravel](https://laravel.com), 
you can use this software to validate your data easily and softly.

## quict start

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
        
        
    validator = LoginValidator({'username': 'michael', 'password': '12345678'})
    status = validator.validate()
    if status:
        print("login succeed")
    else:
        message = validator.get_message()
        print(message)
```