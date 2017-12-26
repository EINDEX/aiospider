#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : config.py
@Created       : 21/12/2017
"""
from tools.singleton import Singleton


class Config(metaclass=Singleton):
    redis_conn = 'redis://localhost:6379'

