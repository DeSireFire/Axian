#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/29
# CreatTIME : 14:46
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import random
from nonebot import get_driver

# 设置信息字典
config_dict = get_driver().config.dict()

def setting_api_key():
    """
    从设置中，获取api_key
    选取时的负载均衡或者复杂的处理逻辑可在该函数中补充
    :return: str，openai的key
    """
    api_keys = config_dict.get('openai_api_key')
    return random.choice(api_keys)

def setting_proxies():
    """
    从设置中，获取代理设置
    选取时的负载均衡或者复杂的处理逻辑可在该函数中补充
    :return: str，代理ip地址
    """
    proxy_ip = config_dict.get('openai_http_proxy')
    return {
        "http": f"{proxy_ip}",
        "https": f"{proxy_ip}",
    }

def setting_chat_limit():
    """
    从设置中，获取最大聊天长度
    选取时的负载均衡或者复杂的处理逻辑可在该函数中补充
    :return: int，大聊天长度
    """
    chat_limit = config_dict.get('openai_chat_limit', 30)
    return int(chat_limit)

