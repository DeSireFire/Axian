#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/30
# CreatTIME : 17:22
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import redis


class RedisList:
    def __init__(self, host, port, db, password=None):
        self.redis = redis.Redis(host=host, port=port, db=db, password=password)

    def add(self, key, value, score):
        self.redis.zadd(key, {value: score})

    def remove(self, key, value):
        self.redis.zrem(key, value)

    def update(self, key, value, score):
        self.redis.zadd(key, {value: score}, xx=True)

    def get_range(self, key, start, end):
        return self.redis.zrange(key, start, end)

    def get_by_score(self, key, min_score, max_score):
        return self.redis.zrangebyscore(key, min_score, max_score)


if __name__ == '__main__':
    REDIS_HOST = '192.168.60.122'
    REDIS_PORT = 6380
    rdb = RedisList(REDIS_HOST, REDIS_PORT, 9)
    print(rdb.add("test", "{233:777}", 0))
    print(rdb.get_by_score("test", 0, 10))
