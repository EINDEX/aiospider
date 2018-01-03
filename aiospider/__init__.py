#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : __init__.py.py
@Created       : 26/12/2017
"""

from aiospider.tools.singleton import OnlySingleton


class AIOSpider(metaclass=OnlySingleton):
    def __init__(self, loop):
        self.config = dict()
        self.loop = loop

    def __eq__(self, other):
        return id(self.config) == id(other.config)

    def __repr__(self):
        return ""
