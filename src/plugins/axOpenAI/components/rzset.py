#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/30
# CreatTIME : 17:22
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import json

import redis


class RedisZset:
    def __init__(self, host, port, db):
        self.pool = redis.ConnectionPool(
            host=host, port=port, db=db, decode_responses=True, health_check_interval=30)
        self.conn = redis.Redis(connection_pool=self.pool)

    def add(self, key, value, score):
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
        for score, i in enumerate(value, start=1):
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
        return self.conn.zrangebyscore(key, 0, self.conn.zcard(key) or 0)


# class RedisSet:
#     def __init__(self, host, port, db):
#         self.pool = redis.ConnectionPool(host=host, port=port, db=db, decode_responses=True, health_check_interval=30)
#         self.conn = redis.Redis(connection_pool=self.pool)
#
#     def add(self, key, value):
#         """
#         添加单条
#         :param key:
#         :param value:
#         :return:
#         """
#         # 字典反序列化，添加
#         if isinstance(value, (tuple, list, dict)):
#             value = json.dumps(value, ensure_ascii=False)
#         # 其它类型的变量直接添加
#         return self.conn.sadd(key, value)
#
#     def add_all(self, key, value):
#         """
#         添加多条
#         :param key:
#         :param value:
#         :param ex: 过期时间，半小时
#         :return:
#         """
#         # 元组列表逐条序列化，批量添加
#         dumps_datas = []
#         for i in value:
#             data_json = json.dumps(i, ensure_ascii=False)
#             dumps_datas.append(data_json)
#         self.conn.sadd(key, *dumps_datas)
#
#     def remove(self, key, value):
#         # 字典反序列化，添加
#         if isinstance(value, (tuple, list, dict)):
#             value = json.dumps(value, ensure_ascii=False)
#         return self.conn.srem(key, value)
#
#     def get(self, key):
#         return self.conn.smembers(key)
#
#     def get_all(self, key):
#         temp = self.conn.smembers(key) or None
#         if isinstance(temp, (list, set)):
#             temp = [json.loads(i) for i in temp]
#         return temp
#
#     def exists(self, key, value):
#         return self.conn.sismember(key, value)
#
#     def __del__(self):
#         self.conn.close()


if __name__ == '__main__':
    REDIS_HOST = '192.168.60.122'
    REDIS_PORT = 6380
    rdb = RedisZset(REDIS_HOST, REDIS_PORT, 9)
    print(rdb.add_all("ax:chat_chain:group_813781752_10252127791", [
        {"233": 233},
        {"666": 666},
    ]))
    print(rdb.get("ax:chat_chain:group_813781752_10252127791", 0))
    print(rdb.get_all("ax:chat_chain:group_813781752_10252127791"))
    print(rdb.remove("ax:chat_chain:group_813781752_10252127791", {"233": 233}))

    # rdb = RedisSet(REDIS_HOST, REDIS_PORT, 9)
    # a = rdb.add_all("test2", [{"role": "user", "content": "7888"},{"role": "user", "content": "4455"}], ex=30)
    # print(a)
    # g = rdb.get_all("test2")
    # print(type(g))
    # print(g)
    # g = rdb.remove("test2", {"role": "user", "content": "7888"})
    # print(g)
