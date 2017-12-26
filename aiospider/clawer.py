#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : clawer.py
@Created       : 22/12/2017
"""
import asyncio

from aiospider.request import Bot
from aiospider.tools import RedisPool


async def start():
    bot_dict = {}
    # conn = (await RedisPool.get_pool()).pool
    while True:
        conn = await RedisPool.get_pool().pool
        accounts = await conn.execute('smembers', 'account_token')
        for account in accounts:
            account = account.decode()
            if not bot_dict.get(account):
                bot_dict[account] = Bot(headers={'Authorization': account})
                asyncio.gather(bot_dict[account].start('zhihu:request'))
        await asyncio.sleep(1)
        print(bot_dict)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())
    loop.close()
