#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : test_pytest.py
@Created       : 26/12/2017
"""
import asyncio
import time

from aiospider import AIOSpider
from aiospider.tools.bloom_tools import BloomFilter
from aiospider.tools.job_queue import JobQueue
from aiospider.tools.redis_pool import RedisPool
from aiospider.workers import Worker

loop = asyncio.get_event_loop()


def test_config():
    app = AIOSpider(loop)
    app.config['redis_conn'] = 'redis://localhost:6379/2'
    assert app.config['redis_conn'] == 'redis://localhost:6379/2'


def test_redis():
    app = AIOSpider(loop)
    app.config['redis_conn'] = 'redis://localhost:6379/2'
    pool = RedisPool(app=app)
    pool3 = RedisPool(app=app)

    async def test_pool():
        pool2 = await pool.pool
        pool4 = await pool3.pool
        assert pool2 == pool4
        # res = await pool2.execute('bf.add', 'test', '1')

    # loop = asyncio.get_event_loop()
    loop.run_until_complete(test_pool())
    # loop.close()


def test_queue():
    app = AIOSpider(loop)
    app.config['redis_conn'] = 'redis://localhost:6379/2'
    # rp = RedisPool(app=app)
    jq = JobQueue(app, 'test')

    async def test_pool():
        print(await jq.push('1'))
        assert await jq.get() == b'1'

    # loop = asyncio.get_event_loop()
    loop.run_until_complete(test_pool())
    # loop.close()


def test_bloom():
    app = AIOSpider(loop)
    app.config['redis_conn'] = 'redis://localhost:6379/2'
    # rp = RedisPool(app=app)
    bf = BloomFilter(app, 'test_bloom')
    s = str(int(time.time()))

    async def test_pool():
        print(await bf.add(s))
        print(await bf.exists(s))
        assert await bf.exists(s) == 1

    loop.run_until_complete(test_pool())
    # loop.close()


def test_worker():
    app = AIOSpider(loop)
    queue = Worker(app).req_queue
    print(queue)


def test_aiospider():
    app = AIOSpider(loop)
    app2 = AIOSpider(2)
    assert app == app2


def test_job():
    app = AIOSpider(loop)
    app.config['redis_conn'] = 'redis://localhost:6379/2'
    # rp = RedisPool(app=app)
    bf = BloomFilter(app, 'test_bloom')
    s = str(int(time.time()))

    async def test_pool():
        print(await bf.add(s))
        print(await bf.exists(s))
        assert await bf.exists(s) == 1

    loop.run_until_complete(test_pool())


if __name__ == '__main__':
    # test_config()
    # test_redis()
    test_worker()
