#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
        name='aiospider',
        version='0.0.4',
        url='https://zhuanlan.zhihu.com/p/26159930',
        license='MIT License',
        install_requires=['cchardet', 'aiodns', 'aiohttp', 'async-timeout', 'aioredis'],

        author='EINDEX',
        author_email='hi@eindex.me',

        packages=find_packages(),
        platforms='any',
)
