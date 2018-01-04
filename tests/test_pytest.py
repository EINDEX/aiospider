#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : test_pytest.py
@Created       : 26/12/2017
"""
import asyncio
import logging
import time

from aiospider import AIOSpider
from aiospider.models.job import ResponseJob
from aiospider.request.request import Bot
from aiospider.tools.bloom_tools import BloomFilter
from aiospider.tools.job_queue import JobQueue
from aiospider.tools.redis_pool import RedisPool
from aiospider.workers import Worker

loop = asyncio.get_event_loop()
app = AIOSpider(loop)
app.config['redis_conn'] = 'redis://localhost:6379/2'


def test_config():
    assert app.config['redis_conn'] == 'redis://localhost:6379/2'


def test_redis():
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
    # rp = RedisPool(app=app)
    jq = JobQueue(app, 'test')

    async def test_pool():
        print(await jq.push('1'))
        assert await jq.get() == b'1'

    # loop = asyncio.get_event_loop()
    loop.run_until_complete(test_pool())
    # loop.close()


def test_bloom():
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
    # rp = RedisPool(app=app)
    bf = BloomFilter(app, 'test_bloom')
    s = str(int(time.time()))

    async def test_pool():
        print(await bf.add(s))
        print(await bf.exists(s))
        assert await bf.exists(s) == 1

    loop.run_until_complete(test_pool())


class TestWorker(Worker):
    name = 'test'
    worker = 'test'
    url_regex = 'http://baidu.com'
    keys = {}
    params = {}

    async def start(self):
        print(f'{self.name}:{self.worker}:Start')
        # while True:
        try:
            queue = self.resp_queue
            content = await queue.get()
            if content:
                resp_job = ResponseJob.from_json(content.decode())
                await self._per_handle(resp_job)
            else:
                await asyncio.sleep(1)

        except Exception as e:
            logging.exception(e)


def test_crawler():
    # rp = RedisPool(app=app)

    async def test_pool():
        await TestWorker.request_builder(keys={}).send()
        bot = Bot()
        asyncio.gather(bot.start('test:test:request'))
        await asyncio.sleep(10)
        bot.status = False
        await TestWorker().start()

    loop.run_until_complete(test_pool())


if __name__ == '__main__':
    # test_config()
    # test_redis()
    test_crawler()
