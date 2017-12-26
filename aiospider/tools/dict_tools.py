#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Author        : EINDEX Li
@File          : dict_tools.py
@Created       : 22/12/2017
"""


def get_info(dic: dict or list, parser, default=None):
    temp = dic
    for index, token in enumerate(parser.split('.')):
        if isinstance(temp, list):
            unused_parsing = '.'.join(parser.split('.')[index:])
            return [get_info(t, unused_parsing) for t in temp]
        if temp.get(token):
            temp = temp.get(token)
        elif temp.get(token) in [False, dict(), list()]:
            return temp.get(token)
        else:
            return default
    return temp
