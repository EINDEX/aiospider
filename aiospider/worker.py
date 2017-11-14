#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : Worker.py
@Created       : 2017/11/13
"""


class Worker:
    def __init__(self, client):
        self.client = client

    async def __aenter__(self):
        self.client.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
