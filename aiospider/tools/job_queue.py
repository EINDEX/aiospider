#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : queue.py
@Created       : 21/12/2017
"""
from aiospider import AIOSpider
from aiospider.tools.redis_pool import RedisPool
from aiospider.tools.singleton import Singleton


class JobQueue(metaclass=Singleton):
    def __init__(self, app, name):
        self._app = app
        self.name = name
        self.pool = None

    @property
    def app(self):
        if not self._app:
            self._app = AIOSpider(None)
        return self._app

    async def push(self, *items, reverse=False):
        if not self.pool:
            self.pool = await RedisPool(self.app).pool
        # calling methods of Redis class
        command = f'{"r" if reverse else "l"}push'
        return await self.pool.execute(command, self.name, *items)

    async def get(self, reverse=False):
        if not self.pool:
            self.pool = await RedisPool(self.app).pool
        command = f'{"l" if reverse else "r"}pop'
        return await self.pool.execute(command, self.name)
