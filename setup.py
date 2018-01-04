#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
        name='aiospider',
        version='0.0.9',
        description='A spider use asyncio.',
        license='MIT License',
        install_requires=['cchardet', 'aiodns', 'aiohttp', 'async-timeout', 'aioredis'],

        author='EINDEX',
        author_email='hi@eindex.me',
        python_requires='>=3.6',
        packages=find_packages(),
        platforms='any',
)
