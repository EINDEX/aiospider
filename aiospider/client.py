#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : Client.py
@Created       : 2017/11/13
"""
from functools import partial, wraps

import aiohttp
import async_timeout

from ._exception import ClientNoSessionException


def req_timeout(timeout=20):
    def decorate(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            with async_timeout.timeout(timeout):
                return await func(*args, **kwargs)

        return wrapper

    return decorate


class Client:
    def __init__(self, headers=None, cookies=None, proxy=None, session=None, loop=None):
        # init
        self._headers = headers
        self._cookies = cookies
        self.loop = loop
        self._proxy = proxy
        self.session = session
        if self.session:
            self.__init()

    def __init(self):
        if not self.session:
            raise ClientNoSessionException()
        self.head = partial(self.session.head, proxy=self._proxy)
        self.get = partial(self.session.get, proxy=self._proxy)
        self.post = partial(self.session.post, proxy=self._proxy)
        self.put = partial(self.session.put, proxy=self._proxy)
        self.patch = partial(self.session.patch, proxy=self._proxy)
        self.delete = partial(self.session.delete, proxy=self._proxy)
        self.options = partial(self.session.options, proxy=self._proxy)

    def __enter__(self):
        self.closed = False
        self.session = aiohttp.ClientSession(headers=self._headers, cookies=self._cookies, loop=self.loop)
        self.__init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def close(self):
        self.session.close()
