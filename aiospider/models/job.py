#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : job.py
@Created       : 21/12/2017
"""
import json

from aiospider.tools.job_queue import JobQueue
from aiospider.tools.redis_pool import RedisPool


class RequestJob:
    def __init__(self,
                 worker,
                 url,
                 method='GET',
                 params=None,
                 data=None,
                 keys=None,
                 identity=None,
                 headers=None,
                 cookies=None,
                 proxy=None,
                 name=None,
                 allow_redirect=None,
                 redirect_times=None):
        self.url = url
        self.keys = keys
        self.params = params
        self.data = data
        self.method = method
        self.headers = headers
        self.cookies = cookies
        self.proxy = proxy
        self.allow_redirect = allow_redirect
        self.redirect_times = redirect_times
        self.identity = identity
        self.worker = worker
        self.name = name

    def to_dict(self):
        content = {}
        for k, v in self.__dict__.items():
            if v:
                content[k] = v
        return content

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    async def bloom_filter(name, worker, url, params=None, **kwargs):
        pool = await RedisPool.get_pool().pool
        if params:
            key = f'{url}{sorted(params.items())}'
        else:
            key = f'{url}'
        return await pool.execute('sismember', f'{name}:{worker}:filter', key)

    async def send(self):
        content = {}
        for k, v in self.__dict__.items():
            if v:
                content[k] = v
        if not await self.bloom_filter(**content):
            queue = await JobQueue.get_queue(f'{self.name}:{self.worker}:request')
            await queue.push(json.dumps(content))
            return True
        else:
            return False

    def get_request_params(self):
        return {
            'url': self.url,
            'params': self.params,
            'headers': self.headers,
            'method': self.method,
            'proxy': self.proxy,
            'data': self.data,
            'allow_redirects': self.allow_redirect,
            'max_redirects': self.redirect_times,
        }

    @staticmethod
    def from_json(content):
        return RequestJob(**json.loads(content))

    def __repr__(self):
        return self.to_json()


class ResponseJob:
    def __init__(self,
                 request_job: dict or RequestJob,
                 url,
                 worker,
                 name,
                 success,
                 identity=None,
                 content=None,
                 content_type=None,
                 status_code=None,
                 cookies=None,
                 proxy=None):
        if isinstance(request_job, dict):
            self.request_job = RequestJob(**request_job)
        elif isinstance(request_job, RequestJob):
            self.request_job = request_job
        self.url = url
        self.identity = identity
        self.worker = worker
        self.name = name
        self.status_code = status_code
        self.content = content
        self.cookies = cookies
        self.content_type = content_type
        self.success = success
        self.proxy = proxy

    def to_dict(self):
        content = {}
        for k, v in self.__dict__.items():
            if v:
                if isinstance(v, RequestJob):
                    v = v.to_dict()
                content[k] = v
        return content

    def to_json(self):
        return json.dumps(self.to_dict())

    async def send(self):
        queue = await JobQueue.get_queue(f'{self.name}:{self.worker}:response')
        await queue.push(self.to_json())

    @staticmethod
    def from_json(content):
        return ResponseJob(**json.loads(content))
