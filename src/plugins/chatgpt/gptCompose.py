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

    def askChatGPT(self, messages):
        pass


class OpenAIOfficial(OpenAIBase):
    """
    官方openai模块
    """
    def askChatGPT(self, messages):
        """
        快速问答ChatGPT
        :param messages: dict,openAi格式的字典数据
        :return:
        """
        openai.api_key = random.choice(self.api_keys)
        openai.proxy = self.proxies
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=1)
        return response['choices'][0]['message']['content']
