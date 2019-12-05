# PROJECT : django-easy-validator
# TIME    : 18-1-2 上午9:44
# AUTHOR : Younger Shen
# EMAIL : younger.x.shen@gmail.com
# CELL : 13811754531
# WECHAT : 13811754531
# https://github.com/youngershen/

SECRET_KEY = "@1o4_s8+lfapx2%c7azo6orns9p-o#9(b$96mkf#+3+kt1(gl_"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'validator',
    'pytest_django'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'validators',
    }
}

