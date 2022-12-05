#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/6/15
# CreatTIME : 15:39 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

"""
常用网页解析器
"""
from jsonpath import jsonpath

class jsonPath_detail(object):
    """
    json 路径解析 by RQ

    举例：
        获取 json_raw 字典下，键名为complexName的值
        jsonPath_detail(json_raw, ["complexName"]).get()    # 获取第一个值
        jsonPath_detail(json_raw, ["complexName"]).getall() # 获取所有键名为complexName的值，返回列表

    :param json_data: dict,需要采集的字典
    :param names: list,字典的key的名称历史
    :return:
    """

    def __init__(self, json_data, parse_raw):
        self.json_data = json_data
        self.parse_raw = parse_raw
        if isinstance(parse_raw, list):
            self.raw_parse = self.jsonpath_parse_names(self.json_data, self.parse_raw) or None
        if isinstance(parse_raw, str):
            self.raw_parse = self.jsonpath_parse_jpstr(self.json_data, self.parse_raw) or None

    def jsonpath_parse_names(self, json_data, names):
        """
        json 解析报错记录
        :param json_data: dict,需要采集的字典
        :param names: list,字典的key的名称历史
        :return:
        """
        res = jsonpath(json_data, f'$..[{",".join(names)}]')
        # print(f'$..[{",".join(names)}]')
        if isinstance(res, list) and len(res) == 1 and isinstance(res[0], list):
            return res[0]
        return res

    def jsonpath_parse_jpstr(self, json_data, jsonPath_str):
        """
        json 解析报错记录
        :param json_data: dict,需要采集的字典
        :param jsonPath_str: str,jsonpath 语句
        :return:
        """
        res = jsonpath(json_data, f'{jsonPath_str}')
        # print(f'$..[{",".join(names)}]')
        if isinstance(res, list) and len(res) == 1 and isinstance(res[0], list):
            return res[0]
        return res

    def get(self):
        if self.raw_parse and isinstance(self.raw_parse, list) and len(self.raw_parse) >= 1:
            return self.raw_parse[0]
        else:
            return None

    def getall(self):
        return self.raw_parse or []