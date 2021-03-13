#!/usr/bin/python3
from distutils.core import setup

setup(
    name='bt_scraper',
    version='1.0',
    packages=['bt_scraper',],
    entry_points={
    'console_scripts': [
        'bt_scraper = null',
    ],
},
)
