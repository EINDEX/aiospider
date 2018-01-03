#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : config.py
@Created       : 21/12/2017
"""
import json

from aiospider.tools.singleton import Singleton


class Config(metaclass=Singleton):
    def __init__(self, redis_conn):
        self.redis_conn = redis_conn

    @classmethod
    def get_config(cls, src=None):
        conf = None
        if src:
            with open(src, 'r') as f:
                conf = json.loads(f.read())
        return Config(redis_conn=conf['redis_url'])
