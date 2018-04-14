# coding=utf-8
from setuptools import setup, find_packages

setup(
    name='cbake',
    version='0.1.0',
    py_modules=['cbake'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pychalk',
        'pyyaml'
    ],
    package_data={'': ['*.txt', '*.lst']},
    entry_points='''
        [console_scripts]
        cbake=cbake:main
    ''',
    test_suite='nose.collector',
    tests_require=['nose'],
)