#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : test.py
@Created       : 2017/11/13
"""

import asyncio
from asyncio import Queue

import functools

from aiospider.tools import make_future


class Crawler:
    def __init__(self, senders=1, workers=1, loop=None):
        self.senders = senders
        self.workers = workers
        self.queue = Queue(loop=loop)
        self.loop = loop

    async def crawl(self):
        # asyncio.ensure_future(self.sender())
        # a.add_done_callback(functools.partial(print, "Future:", flush=True))
        self.sender(callbacks=[functools.partial(print, "Future:", flush=True)])
        self.worker(callbacks=[functools.partial(print, "Future:", flush=True)])
        while True:
            await asyncio.sleep(1)
            # print(s[0].result)
            # print(a)
            # print(b)
            for x in asyncio.Task.all_tasks():
                print(x._state, x._coro.cr_code.co_name)
                # print(s[0])
                # print(c[0])
                # print('master')

    @make_future
    async def worker(self):
        # while True:
        print(1)
        await asyncio.sleep(2)

    @make_future
    async def sender(self):
        # while True:
        print(0)
        await asyncio.sleep(3)
        # raise Exception('eeee')
        # return 1


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(Crawler(loop=loop).crawl())
    try:
        loop.run_forever()
    except KeyboardInterrupt as e:
        print(asyncio.gather(*asyncio.Task.all_tasks()).cancel())
        loop.stop()
        loop.run_forever()
    finally:
        loop.close()
