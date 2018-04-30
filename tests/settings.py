# PROJECT : hhcms
# TIME : 18-4-30 下午4:57
# AUTHOR : 申延刚 <Younger Shen>
# EMAIL : younger.shen@hotmail.com
# CELL : 13811754531
# WECHAT : 13811754531
SECRET_KEY = "@1o4_s8+lfapx2%c7azo6orns9p-o#9(b$96mkf#+3+kt1(gl_"

INSTALLED_APPS = [
    'validator',
    'pytest_django'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'validators',
    }
}

