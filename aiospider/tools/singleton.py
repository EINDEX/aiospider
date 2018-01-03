#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : singleton.py
@Created       : 21/12/2017
"""


class OnlySingleton(type):
    def __init__(cls, name, bases, attrs):
        super(OnlySingleton, cls).__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(OnlySingleton, cls).__call__(*args, **kwargs)
        return cls._instance


class Singleton(type):
    def __init__(cls, name, bases, attrs):
        super(Singleton, cls).__init__(name, bases, attrs)
        cls._instance = {}

    def __call__(cls, *args, **kwargs):
        key = cls.key_gen(*args, **kwargs)
        cls._instance.setdefault(key, None)
        if cls._instance[key] is None:
            cls._instance[key] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[key]

    @staticmethod
    def key_gen(*args, **kwargs):
        return f'{args}:{kwargs.items()}'
