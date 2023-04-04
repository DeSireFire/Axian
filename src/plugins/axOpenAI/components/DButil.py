#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/30
# CreatTIME : 16:32
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import redis
import os
import time
import json
from src.plugins.axOpenAI.utils import *

# 实例化连接池
# try:
#     rdb_pool = redis.ConnectionPool(
#                 host=setting_redis_host(),
#                 port=setting_redis_port(),
#                 db=setting_redis_db(),
#                 password=setting_redis_password(),
#                 decode_responses=True,
#                 health_check_interval=30,
#                 max_connections=100
#             )
# except Exception as e:
#     print(f"链接redis数据库发生错误！错误信息：{e}")

class RedisZset:
    def __init__(
            self,
            REDIS_DB=setting_redis_db(),
            REDIS_PW=setting_redis_password()
    ):
        self.rdb_pool = redis.ConnectionPool(
            host=setting_redis_host(),
            port=setting_redis_port(),
            db=REDIS_DB,
            password=REDIS_PW,
            decode_responses=True,
            health_check_interval=30,
            max_connections=100
        )
        self.rkey = "ax:chat_chain:"
        # 链接池获取链接
        self.conn = redis.Redis(connection_pool=self.rdb_pool)

    def add(self, key, value, score=None):
        """
        添加单条
        :param key:
        :param value:
        :return:
        """
        if not score:
            score = self.conn.zcard(key) or 0
        # 字典反序列化，添加
        if isinstance(value, (tuple, list, dict)):
            value = json.dumps(value, ensure_ascii=False)
        # 其它类型的变量直接添加
        return self.conn.zadd(key, {value: score})

    def add_all(self, key, value):
        """
        添加多条
        :param key:
        :param value:
        :param ex: 过期时间，半小时
        :return:
        """
        # 元组列表逐条序列化，批量添加
        dumps_datas = {}
        start = self.conn.zcard(key) or 0
        for score, i in enumerate(value, start=start):
            data_json = json.dumps(i, ensure_ascii=False)
            dumps_datas[data_json] = score
        return self.conn.zadd(name=key, mapping=dumps_datas)

    def remove(self, key, value):
        value = json.dumps(value, ensure_ascii=False)
        return self.conn.zrem(key, value)

    def update(self, key, value, score):
        return self.conn.zadd(key, {value: score}, xx=True)

    def get(self, key, index):
        return self.conn.zrange(key, index, index)

    def get_all(self, key):
        temp = self.conn.zrangebyscore(key, 0, self.conn.zcard(key) or 0)
        if isinstance(temp, (list, set)):
            temp = [json.loads(i) for i in temp]
        return temp

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


class JsonFileManager:
    def __init__(self, file_path, expiration_time=0):
        self.file_path = file_path
        self.expiration_time = expiration_time
        self.data = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self.data = json.load(f)

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f)

    def add_data(self, key, value):
        self.data[key] = value
        self.save_data()

    def delete_data(self, key):
        if key in self.data:
            del self.data[key]
            self.save_data()

    def update_data(self, key, value):
        if key in self.data:
            self.data[key] = value
            self.save_data()

    def get_data(self, key):
        return self.data.get(key)

    def check_expiration(self):
        if self.expiration_time > 0:
            current_time = time.time()
            file_time = os.path.getmtime(self.file_path)
            if current_time - file_time > self.expiration_time:
                os.remove(self.file_path)


if __name__ == '__main__':
    file_manager = JsonFileManager('example.json', 3600)
    file_manager.add_data('name', 'John')
    file_manager.add_data('age', 30)
    print(file_manager.get_data('name'))
    file_manager.update_data('age', 31)
    file_manager.delete_data('name')
    file_manager.check_expiration()
