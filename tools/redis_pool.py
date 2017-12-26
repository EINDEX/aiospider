#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : redis_pool.py
@Created       : 21/12/2017
"""
import aioredis
import asyncio

from tools.singleton import Singleton


class RedisPool(metaclass=Singleton):
    def __init__(self, redis_url):
        self.redis_url = redis_url
        self._pool = None

    @property
    async def pool(self):
        if not self._pool:
            self._pool = await aioredis.create_connection(self.redis_url)
        return self._pool

    @classmethod
    def get_pool(cls):
        return RedisPool(redis_url='redis://localhost:6379/2')


if __name__ == '__main__':
    async def test():
        x = RedisPool.get_pool()
        x1 = RedisPool.get_pool()
        x2 = RedisPool.get_pool()
        x3 = RedisPool.get_pool()
        x4 = RedisPool.get_pool()
        x5 = RedisPool.get_pool()
        print(await x.pool)
        print(await x1.pool)
        print(await x2.pool)
        print(await x3.pool)
        print(await x4.pool)
        print(await x5.pool)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.close()
