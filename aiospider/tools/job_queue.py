#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : queue.py
@Created       : 21/12/2017
"""
import asyncio

from aiospider.tools.redis_pool import RedisPool
from aiospider.tools.singleton import Singleton


class JobQueue(metaclass=Singleton):
    def __init__(self, name, pool):
        self.name = name
        self.pool = pool

    @staticmethod
    async def get_queue(name):
        pool = await RedisPool.get_pool().pool
        return JobQueue(name=name, pool=pool)

    async def push(self, *items, reverse=False):
        # calling methods of Redis class
        command = f'{"r" if reverse else "l"}push'
        return await self.pool.execute(command, self.name, *items)

    async def get(self, reverse=False):
        command = f'{"l" if reverse else "r"}pop'
        return await self.pool.execute(command, self.name)


if __name__ == '__main__':
    async def test():
        x = await JobQueue.get_queue('test')
        x1 = await JobQueue.get_queue('test')
        print(x)
        print(x1)
        print(x is x1)
        await x.push('1')
        print(await x.get())


    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.close()
