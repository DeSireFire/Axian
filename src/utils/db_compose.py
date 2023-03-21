#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/21
# CreatTIME : 11:02
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
import redis
import json
REDIS_HOST = '192.168.60.122'
REDIS_PORT = 6380

class RedisDBHelper(object):
    def __init__(self, db=0):
        self.pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=db,
                                         decode_responses=True, health_check_interval=30)
        self.server = redis.Redis(connection_pool=self.pool)

    def __del__(self):
        self.server.close()

    def get(self, redis_key):
        return self.server.get(redis_key)

    def sadd(self, redis_key, data):
        if isinstance(data, (tuple, list, dict)):
            data = json.dumps(data, ensure_ascii=False)
        return self.server.sadd(redis_key, data)

    def srem(self, redis_key, data):
        if isinstance(data, (tuple, list, dict)):
            data = json.dumps(data, ensure_ascii=False)
        return self.server.srem(redis_key, data)

    def sismember(self, name, value):
        return self.server.sismember(name, value)

    def smembers(self, name):
        return self.server.smembers(name)

    def spop(self, redis_key, count=None):
        return self.server.spop(redis_key, count)

    def rpush(self, redis_key, val):
        return self.server.rpush(redis_key, val)

    def blpop(self, redis_key, timeout=0):
        return self.server.blpop(redis_key, timeout)

    def pop_list_queue(self, redis_key, batch_size):
        with self.server.pipeline() as pipe:
            pipe.lrange(redis_key, 0, batch_size - 1)
            pipe.ltrim(redis_key, batch_size, -1)
            datas, _ = pipe.execute()
        return datas

    def lrange(self, name, start, end):
        return self.server.lrange(name, start, end)

    def lpush(self, name, value):
        if isinstance(value, (tuple, list, dict)):
            value = json.dumps(value, ensure_ascii=False)
        return self.server.lpush(name, value)

    def set(self, name, value):
        if isinstance(value, (tuple, list, dict)):
            value = json.dumps(value, ensure_ascii=False)
        return self.server.set(name, value)

    def incr(self, name, *value):
        return self.server.incr(name, *value)

    def exists(self, name):
        return self.server.incr(name)