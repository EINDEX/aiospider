#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : request.py
@Created       : 21/12/2017
"""
import logging

import aiohttp
import asyncio

from job import ResponseJob, RequestJob
from aiospider.tools import JobQueue
from aiospider.tools import RedisPool


class Bot:
    def __init__(self, bot_id=None, headers=None, cookies=None, proxy=None, status=False, loop=None):
        self.bot_id = bot_id
        self._session = None
        self.headers = headers
        self.cookies = cookies
        if not proxy:
            self._proxy = 'http://lum-customer-hl_b9fea07e-zone-zone8:8lvtlx73qqnu@zproxy.luminati.io:22225'
        self._proxy = proxy
        self.loop = loop
        self.status = False

    @property
    def session(self):
        if not self._session:
            return aiohttp.ClientSession(headers=self.headers, cookies=self.cookies, loop=self.loop)
        return self._session

    async def __aenter__(self):
        return self

    def __enter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.close()

    def close(self):
        if self._session:
            self._session.close()
        return True

    @staticmethod
    async def request(session, method, url, *args, **kwargs):
        async with session.request(method, url, *args, **kwargs) as resp:
            return resp.status, await resp.text()

    async def start(self, name):
        try:
            self.status = True
            queue = await JobQueue.get_queue(name)

            async with self.session as session:
                while True:
                    item = await queue.get()
                    if item:
                        item = item.decode()
                        try:
                            req_job = RequestJob.from_json(item)

                            if req_job.params:
                                key = f'{req_job.url}{sorted(req_job.params.items())}'
                            else:
                                key = f'{req_job.url}'
                            pool = await RedisPool.get_pool().pool
                            if await pool.execute('sismember', f'{req_job.name}:{req_job.worker}:filter', key):
                                continue
                            # if req_job.worker not in ['followees', 'person', 'following']:
                            #     await pool.execute('lpush', 'zhihu:later:request', req_job.to_json())
                            #     continue
                        except Exception as e:
                            logging.exception(e)
                            continue
                        try:
                            req_job.headers.update(self.headers)
                            status, content = await self.request(session, **req_job.get_request_params())
                            print(status, content)
                            await ResponseJob(request_job=req_job, url=req_job.url, worker=req_job.worker,
                                              name=req_job.name,
                                              success=True,
                                              status_code=status,
                                              content=content).send()
                        except Exception as e:
                            req_job.send()
                            logging.exception(e)
                        await asyncio.sleep(0.6)
        except Exception as e:
            logging.exception(e)
            self.status = False


if __name__ == '__main__':
    async def test():
        inner_queue = asyncio.Queue(maxsize=100, loop=loop)
        b = Bot('key', {}, {}, inner_queue, loop=loop)
        await b.start(name='zhihu:request')
        await inner_queue.join()


    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
    loop.close()
