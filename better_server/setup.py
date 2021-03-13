#!/usr/bin/python3
from distutils.core import setup

setup(
    name='bt_server',
    version='1.0',
    packages=['bt_server',]
    entry_points={
    'console_scripts': [
        'bt_server = null',
    ],
},
)
