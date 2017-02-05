#!/usr/bin/env python

from setuptools import setup

setup(name='predominantmelodymakam',
    description='Predominant melody extraction of makam music',
    version='1.2.2',
    author='Sertan Senturk',
    author_email='contact AT sertansenturk DOT com',
    license='agpl 3.0',
    url='http://sertansenturk.com',
    packages=['predominantmelodymakam'],
    install_requires=[
        "numpy",
        "scipy"
    ],
)
