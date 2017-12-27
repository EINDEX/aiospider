#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : base_worker.py
@Created       : 22/12/2017
"""
import asyncio
import logging

from aiospider.models.job import RequestJob, ResponseJob
from aiospider.tools.job_queue import JobQueue


class Worker:
    keys = {}
    name = None
    worker = None
    url_regex = None
    method = None
    params = {}
    require_params = []
    headers = {}

    @classmethod
    async def analyze(cls, request_job: RequestJob, content):
        pass

    @staticmethod
    def parser(data: dict):
        pass

    @staticmethod
    def pre_handle(resp_job: ResponseJob):
        return True

    @classmethod
    async def _per_handle(cls, resp_job: ResponseJob):
        if cls.pre_handle(resp_job):
            return await cls.analyze(request_job=resp_job.request_job, content=resp_job.content)
        else:
            raise ValueError()

    @classmethod
    def request_builder(cls, keys: dict, params=None, headers=None, data=None, identity=None,
                        redirect_times=None,
                        allow_redirect=None,
                        proxy=None,
                        cookies=None):
        url = cls.url_regex
        for key, value in keys.items():
            url = cls.url_regex.replace('{%s}' % key, str(value))
        for must in cls.require_params:
            if must not in params:
                raise ValueError()
        if isinstance(params, dict):
            cls.params.update(params)
        if headers:
            cls.headers.update(headers)
        return RequestJob(worker=cls.worker, url=url, method=cls.method, params=cls.params, data=data,
                          identity=identity, headers=cls.headers,
                          keys=keys,
                          cookies=cookies, proxy=proxy, name=cls.name, allow_redirect=allow_redirect,
                          redirect_times=redirect_times)

    @classmethod
    async def start(cls):
        print(f'{cls.name}:{cls.worker}:Start')
        while True:
            try:
                queue = await JobQueue.get_queue(f'{cls.name}:{cls.worker}:response')
                content = await queue.get()
                if content:
                    resp_job = ResponseJob.from_json(content.decode())
                    await cls._per_handle(resp_job)
                else:
                    await asyncio.sleep(1)

            except Exception as e:
                logging.exception(e)
