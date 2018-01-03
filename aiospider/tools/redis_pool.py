#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : redis_pool.py
@Created       : 21/12/2017
"""
import aioredis

from aiospider import AIOSpider
from aiospider.tools.singleton import OnlySingleton


class RedisPool(metaclass=OnlySingleton):
    def __init__(self, app):
        self._app = app
        self.redis_url = app.config['redis_conn']
        self._pool = None

    @property
    async def pool(self):
        if not self._pool:
            self._pool = await aioredis.create_connection(self.redis_url)
        return self._pool

    @property
    def app(self):
        if not self._app:
            self._app = AIOSpider(None)
        return self._app
