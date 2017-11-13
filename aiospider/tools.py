#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : tools.py
@Created       : 2017/11/13
"""
import asyncio
from functools import wraps


def make_future(func):
    @wraps(func)
    def wrapper(self, callbacks=[], *args, **kwargs):
        future = asyncio.ensure_future(func(self, *args, **kwargs))
        for callback in callbacks:
            future.add_done_callback(callback)
        return future

    return wrapper

