#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
        name='aio_spider',
        version='0.0.3',
        url='https://zhuanlan.zhihu.com/p/26159930',
        license='MIT License',
        install_requires=['aiohttp', 'async-timeout'],

        author='EINDEX',
        author_email='hi@eindex.me',

        packages=find_packages(),
        platforms='any',
)
