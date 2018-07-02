from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='django-easy-validator',

    version='1.0.4',

    description='a very easy use django request POST/GET data validator',

    url='https://github.com/youngershen/django-easy-validator',

    # Author details
    author='Younger Shen',
    author_email='younger.shen@hotmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',

        'Framework :: Django :: 1.6'

    ],

    # What does your project relate to?
    keywords='a django request POST/GET data validator',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    install_requires=[
        'Django',
    ],

    python_requires='>=3.6',

)
