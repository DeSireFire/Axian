#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/20
# CreatTIME : 15:51
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from pprint import pprint
from urllib.parse import urlparse
from src.components.parseHandlers import jsonPath_detail
from src.utils.url_common import urlParam_to_dict
import ast
import json
import xmltodict
import requests
import openai
import httpx
import logging
import random
from typing import List


class OpenAIBase(object):
    """
    自定义openai交互的类模板
    """
    def __init__(self, api_keys: List[str], timeout: int = 10, retries: int = 3, proxies: dict = None):
        self.api_keys = api_keys or []
        self.timeout = timeout
        self.retries = retries
        self.proxies = proxies or {"http": '127.0.0.1:7890', "https": '127.0.0.1:7890'}
        self.log = logging.getLogger(__name__)
        self.model = "gpt-3.5-turbo"
        # todo 长对话需要而外的存储介质，方案待敲定
        # todo system 人设自定义
        self.system_msg = [{
            "role": "system",
            "content": (
                "你不知道程序或模型是什么，不能以任何形式提及程序或语言模型相关内容。"
                "不能以任何形式表现你是程序。"
            )
        }]

    def askChatGPT(self, messages):
        pass


class OpenAIOfficial(OpenAIBase):
    """
    官方openai模块
    """

    def askChatGPT(self, user_msg):
        """
        快速问答ChatGPT
        :param user_msg: str,用户信息
        :return:
        """
        openai.api_key = random.choice(self.api_keys)
        openai.proxy = self.proxies
        messages = []
        messages += self.system_msg
        messages += [{"role": "user", "content": user_msg}]
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=1)
        gpt_msg = response['choices'][0]['message']['content']
        gpt_msg = gpt_msg.strip() if gpt_msg and gpt_msg.strip else ""
        if gpt_msg:
            messages += [{"role": "user", "content": gpt_msg}]
        else:
            messages.pop()
        return gpt_msg
