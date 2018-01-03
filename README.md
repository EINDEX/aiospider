# AioSpider
[![Python](https://img.shields.io/badge/python-3.6-blue.svg?style=flat)]()
[![PyPI](https://img.shields.io/pypi/v/aiospider.svg)]()
[![codecov](https://img.shields.io/codecov/c/github/EINDEX/aiospider/master.svg)](https://codecov.io/gh/EINDEX/aiospider)
[![Build Status](https://img.shields.io/travis/EINDEX/aiospider/master.svg)](https://travis-ci.org/EINDEX/aiospider)
## 架构
### 执行单元
- 执行请求
- 失败重放
- 代理策略配置
- 账号机制
- Session 缓存机制
- 并发量限制
- 单元运行状态监测

### 队列
Redis list

### 代理池
Redis 占时先订上了

### 数据库
- Bloom: Redis

### 任务发布/处理单元
- 统一的处理模块
- 自动分配任务
- 发布任务

## Bug
- 任务堆积过多时，爬虫获取携带代理 IP 在队列中等待时间过长。请求发送时，代理 IP 可能已经失效。

