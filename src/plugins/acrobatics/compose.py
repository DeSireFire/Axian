#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/4/6
# CreatTIME : 13:48
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import redis
import os
import time
import json
from src.plugins.axOpenAI.utils import *


class RedisSet:
    def __init__(
            self,
            REDIS_DB=setting_redis_db(),
            REDIS_PW=setting_redis_password()
    ):
        self.pool = redis.ConnectionPool(
            host=setting_redis_host(),
            port=setting_redis_port(),
            db=REDIS_DB,
            password=REDIS_PW,
            decode_responses=True, health_check_interval=30)
        self.conn = redis.Redis(connection_pool=self.pool)

    def add(self, key, value):
        """
        添加单条
        :param key:
        :param value:
        :return:
        """
        # 字典反序列化，添加
        if isinstance(value, (tuple, list, dict)):
            value = json.dumps(value, ensure_ascii=False)
        # 其它类型的变量直接添加
        return self.conn.sadd(key, value)

    def add_all(self, key, value, *kw):
        """
        添加多条
        :param key:
        :param value:
        :return:
        """
        # 元组列表逐条序列化，批量添加
        dumps_datas = []
        for i in value:
            data_json = json.dumps(i, ensure_ascii=False)
            dumps_datas.append(data_json)
        # 遍历处理以后会发生倒序
        if dumps_datas:
            dumps_datas = dumps_datas[::-1]
        self.conn.sadd(key, *dumps_datas, *kw)

    def remove(self, key, value):
        # 字典反序列化，添加
        if isinstance(value, (tuple, list, dict)):
            value = json.dumps(value, ensure_ascii=False)
        return self.conn.srem(key, value)

    def get(self, key):
        return self.conn.srandmember(key, 1)

    def get_all(self, key):
        temp = self.conn.smembers(key) or None
        if isinstance(temp, (list, set)):
            temp = [json.loads(i) for i in temp]
        return temp

    def exists(self, key, value):
        return self.conn.sismember(key, value)

    def expire(self, key, extime):
        """
        过期时间设置
        :param key:
        :param extime:
        :return:
        """
        return self.conn.expire(key, extime)

    def __del__(self):
        self.conn.close()
