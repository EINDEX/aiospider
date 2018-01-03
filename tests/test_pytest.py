#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : test_pytest.py
@Created       : 26/12/2017
"""
from aiospider.config import Config


def test_pytest():
    conf = Config.get_config('config.json')
    assert conf.redis_conn == 'redis://localhost:6379/2'


if __name__ == '__main__':
    test_pytest()
