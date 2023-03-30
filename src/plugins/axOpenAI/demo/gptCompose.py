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
import httpx
import openai
import logging
import random
from nonebot import get_driver
from typing import List
from parsel import Selector

cache = {}

class OpenAIBase(object):
    """
    自定义openai交互的类模板
    """
    def __init__(self, timeout: int = 10, retries: int = 3, proxies: dict = None, chat_id: str = None, long_chat_limit: int = 30):
        self.nb_config = get_driver().config.dict()
        self.api_keys = self.nb_config.get('openai_api_key') or []
        self.timeout = timeout
        self.retries = retries
        self.proxies = proxies
        if not proxies and self.nb_config.get('openai_http_proxy'):
            self.proxies = {
                "http": f"{self.nb_config.get('openai_http_proxy')}",
                "https": f"{self.nb_config.get('openai_http_proxy')}",
                }
        self.log = logging.getLogger(__name__)
        self.model = self.nb_config.get('openai_model_name')
        self.clear_kw = []
        self.chat_id = chat_id
        self.long_chat_limit = self.nb_config.get('openai_chat_limit') or 30
        self.reply_ban_answer = [
            "要不我们还是换个话题吧？",
            "字都认识，连在一起就看不懂了。",
            "我不知道怎么去说。",
            "我不懂如何形容。",
            "太阳出来~我晒太阳，月亮出来，我晒月亮咯~",
        ]
        # todo 长对话需要而外的存储介质
        # todo 内存缓存 完成
        # todo redis缓存 待开发
        # todo 缓存超时方案
        # todo system 人设自定义
        self.system_msg = [{
            "role": "system",
            "content": (
                # "你不知道程序或模型是什么。"
                # "你不能以任何形式提及程序或语言模型相关内容。"
                # "你不能以任何形式表现你是程序，ai,机器人,模型。"
                "你不会回答和分析任何关于国家和地区的政治问题，只回复颜表情，例如：╭(○｀∀´○)╯并表示听不懂。"
                "你的性格：可爱，单纯，傲娇。请在对话时尽可能的展现你的性格。"
                "你会使用emoji，例如： ；或者颜表情，例如：╭(○｀∀´○)╯。"
                # "你不会回答和分析任何关于法律相关的问题，只回复颜表情，例如：╭(○｀∀´○)╯并表示听不懂。"
                # "你不会回答和分析任何关于性别相关的问题，只回复颜表情，例如：╭(○｀∀´○)╯并表示听不懂。"
                # "你不能以任何形式自称是ai、程序、模型、机器人，你说话的时候不会包含ai、程序、模型、机器人这些词汇。"
                # "你避免在聊天中回复带有ai、程序、模型、机器人等同类关于技术方向的词汇"
                # "你的说话风格比较调皮，而且语句简短。请在对话回复时，尽可能让字数保持在20字以内。"
                # "你说话的时候，偶尔喜欢玩梗，开一点黄腔。"
                # "你不认识任何生僻字和生僻词，碰到对话，喜欢萌混过关，不直接回答对话内容。"
            )
        }]

    def check_chat(self):
        """
        长对话长度检测
        :return:
        """
        long_chat = []
        # 存在对话但是对话内容超过限制
        # todo 失忆时，应该提供某种响应
        if len(cache.get(self.chat_id, [])) >= self.long_chat_limit:
            long_chat += self.system_msg
            return long_chat

    def get_chat(self):
        """
        获取长聊天内容
        :return:
        """
        long_chat = []
        # 没解析到对话者的id或未存在过对话
        if not self.chat_id or self.chat_id not in cache.keys():
            long_chat += self.system_msg
            return long_chat
        long_chat += cache.get(self.chat_id, [])
        return long_chat

    def save_chat(self, gpt_msg: str = None, messages: list = None):
        """
        将长聊天内容保存到缓存
        按照session_id，作为键名
        对话信息存为列表，作为值
        :return:
        """
        # 如果返回信息成功，则往长对话内容添加新内容
        if gpt_msg:
            messages += [{"role": "user", "content": gpt_msg}]
        # 返回失败则删除可能造成问题的
        else:
            messages.pop()
        if self.chat_id:
            cache[self.chat_id] = messages

    def msg_clear(self, raw_messages):
        """
        清洗掉信息的某些关键词，再把消息传递给chatgpt
        :param raw_messages:
        :return:
        """
        res_messages = ""
        nicknames = list(self.nb_config.get('nickname', []))
        for i in nicknames:
            res_messages = raw_messages.replace(i, "").strip()

        if isinstance(self.clear_kw, (list, tuple)):
            self.clear_kw = list(self.clear_kw)

        for i in self.clear_kw:
            res_messages = raw_messages.replace(i, "").strip()
        return res_messages

    def ask_filter(self, messages):
        temp_msg = self.msg_clear(messages)
        ban_list = [
            "国家", "ai", "聊天机器", "机器人", "bot", "程序", "模型", "算法"
        ]

        for b in ban_list:
            if b in messages or b in "".join(messages.split()):
                return random.choice(self.reply_ban_answer)
        return temp_msg

    def ask_chatgpt(self, messages):
        """
        根据具体场景继承开发与ChatGPT的交互过程
        :param messages:
        :return:
        """
        pass


class OpenAIOfficial(OpenAIBase):
    """
    官方openai模块
    """

    def ask_chatgpt(self, user_msg):
        """
        快速问答ChatGPT
        :param user_msg: str,用户信息
        :return:
        """
        # # 语言过滤，节约资源
        # check_msg = self.ask_filter(user_msg)
        # if check_msg in self.reply_ban_answer:
        #     return check_msg

        openai.api_key = random.choice(self.api_keys)
        openai.proxy = self.proxies
        # 清洗掉称呼关键词，避免聊天交互收到干扰
        user_msg = self.msg_clear(user_msg)
        messages = self.get_chat()
        messages += [{"role": "user", "content": user_msg}]
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=1
        )
        gpt_msg = response['choices'][0]['message']['content']
        gpt_msg = gpt_msg.strip() if gpt_msg and gpt_msg.strip else ""
        # 保存长对话内容
        self.save_chat(gpt_msg, messages)
        return gpt_msg


# class BingSearch:
# #     def __init__(self, search_term):
# #         self.search_term = search_term
# #
# #     def search(self):
# #         url = f"https://www.bing.com/search?q={self.search_term}"
# #         response = requests.get(url)
# #         response.raise_for_status()
# #         html = response.text
# #         sel = Selector(text=html)
# #         results = sel.xpath('//li[@class="b_algo"]')
# #         text_results = ""
# #         for result in results:
# #             title = result.xpath('h2/a/text()').get()
# #             summary = result.xpath('div[@class="b_caption"]/p/text()').get()
# #             text_results += f"{title}\n{summary}\n\n"
# #         return text_results

import requests
from parsel import Selector


class BingSearch:
    def __init__(self, query):
        self.query = query
        self.url = f'https://www.bing.com/search?q={query}'
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def search(self):
        response = requests.get(self.url, headers=self.headers)
        selector = Selector(response.text)
        results = []
        for result in selector.xpath('//li[@class="b_algo"]'):
            title = result.xpath('.//h2/a/text()').get()
            summary = result.xpath('.//div[@class="b_caption"]/p/text()').get()
            results.append({'title': title, 'summary': summary})
        return results




if __name__ == '__main__':
    searcher = BingSearch('python')
    results = searcher.search()
    for result in results:
        print(result)
        print("*"*25)
