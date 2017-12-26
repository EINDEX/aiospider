#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : mongodb_pool.py
@Created       : 22/12/2017
"""
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient()
db = client.zhihu
person_c = db.person
