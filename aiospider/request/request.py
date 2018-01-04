#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : request.py
@Created       : 21/12/2017
"""
import logging

import aiohttp
import async_timeout

from aiospider import AIOSpider
from aiospider.models.job import ResponseJob, RequestJob
from aiospider.tools.job_queue import JobQueue


class Bot:
    def __init__(self, bot_id=None, headers=None, cookies=None, proxy=None, status=False, loop=None, app=None):
        self.bot_id = bot_id
        self._session = None
        self.headers = headers
        self.cookies = cookies
        self._proxy = proxy
        self.loop = loop
        self.status = status
        self._app = app

    @property
    def app(self):
        if not self._app:
            self._app = AIOSpider()
        return self._app

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
    async def request(session, timeout, *args, **kwargs):
        with async_timeout.timeout(timeout):
            async with session.request(*args, **kwargs) as resp:
                return resp.status, await resp.text()

    async def start(self, name):
        try:
            self.status = True
            queue = JobQueue(None, name)
            async with self.session as session:
                while True:
                    item = await queue.get()
                    if item:
                        item = item.decode()
                        try:
                            req_job = RequestJob.from_json(item)
                        except Exception as e:
                            logging.exception(e)
                            continue
                        try:
                            status, content = await self.request(session, req_job.timeout,
                                                                 **req_job.get_request_params())
                            resp_job = ResponseJob(request_job=req_job, url=req_job.url, worker=req_job.worker,
                                                   name=req_job.name,
                                                   success=True,
                                                   status_code=status,
                                                   content=content)
                            logging.info(resp_job.to_json())
                            await resp_job.send()
                        except Exception as e:
                            resp_job = ResponseJob(request_job=req_job, url=req_job.url, worker=req_job.worker,
                                                   name=req_job.name,
                                                   success=False,
                                                   status_code=400,
                                                   content='{}')
                            logging.warning(resp_job.to_json())
                            await resp_job.send()
                            logging.error(str(e))
        except Exception as e:
            logging.exception(e)
            self.status = False
