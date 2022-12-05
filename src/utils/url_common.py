#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/10/17
# CreatTIME : 15:17 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from urllib.parse import urlparse


def urlParam_to_dict(url: str) -> dict:
    """
    url的get参数转为 字典
    """
    from urllib.parse import parse_qs
    urlParam_dict = {}
    temp = dict([(k, v[0]) for k, v in parse_qs(urlparse(url).query).items()]) or {}
    if temp:
        urlParam_dict = temp
    return urlParam_dict


def dict_to_urlParam(temp_dict: dict) -> str:
    """
    将字典转为url的get参数
    :param temp_dict: dict, 需要转换的字典
    :return:
    """
    import urllib.parse
    params = urllib.parse.urlencode(temp_dict)
    return params