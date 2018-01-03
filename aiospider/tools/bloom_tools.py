#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : bloom_tools.py
@Created       : 22/12/2017
"""
from aiospider import AIOSpider
from aiospider.tools.redis_pool import RedisPool
from aiospider.tools.singleton import Singleton


class BloomFilter(metaclass=Singleton):
    ADD_COMMAND = 'BF.ADD'
    EXISTS_COMMAND = 'BF.EXISTS'

    def __init__(self, app, name):
        self._app = app
        self.name = name
        self.pool = None

    @property
    def app(self):
        if not self._app:
            self._app = AIOSpider(None)
        return self._app

    async def add(self, key):
        if not self.pool:
            self.pool = await RedisPool(self.app).pool
        return await self.pool.execute(self.ADD_COMMAND, self.name, key)

    async def exists(self, key):
        if not self.pool:
            self.pool = await RedisPool(self.app).pool
        return await self.pool.execute(self.EXISTS_COMMAND, self.name, key)
