#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : workers.py
@Created       : 22/12/2017
"""
import asyncio

# print(workers_mapping)

response_queue_names = []


async def start():
    print('Start')
    print('End')
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    loop.close()
