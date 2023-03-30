#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/29
# CreatTIME : 15:00
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

try:
    import asyncio
    import openai
    import logging
    from src.plugins.axOpenAI.utils import *
    from pprint import pprint
    from ..components.DButil import RedisDBHelper
except Exception as e:
    print(f"导入发生错误：{e}")

# 实例化RedisDBHelper
rdb = RedisDBHelper(9)

class OpenAIBase(object):
    """
    自定义openai交互的类模板

    清洗用户信息
    调取历史对话(检测对话是否存在)
    构造对话数据()
    问询gpt
    更新历史会话
    返回gpt响应信息

    提供长对话获取函数，方便domainant的业务函数获取信息

    """

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.chat_limit = setting_chat_limit()
        self.api_keys = setting_api_key()
        self.proxies = setting_proxies()
        self.timeout = 10
        self.model = None
        self.chat_id = None
        self.input_clear = []
        self.db = rdb

    async def input_message_clear(self, input_msg):
        """
        对输入的信息进行预处理，清洗
        :param input_msg:
        :return:
        """
        if not input_msg or not self.input_clear:
            return input_msg

        for i in self.input_clear:
            input_msg = input_msg.replace(i, "")

        return input_msg

    async def generate_text(self, messages):
        """
        与openai交互
        :param messages: 长对话聊天信息
        :return:
        """
        openai.api_key = self.api_keys
        openai.proxy = self.proxies

        completions = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=messages,
            temperature=1
        )
        message = completions['choices'][0]['message']['content']
        # pprint(message)
        return message

    async def structure_chat(self, input_msg):
        """
        获取&构造对话信息数据体
        :param input_msg: 输入进来等待处理的信息
        :return:
        """
        messages = []
        # 没有信息id,不索引长对话，直接构造返回
        if not self.chat_id:
            messages += [{"role": "user", "content": input_msg}]
            return messages
        # self.db.server.zrem()
        # if self.

        return messages


    async def update_to_save_chat(self, gpt_msg, messages):
        """
        更新&保存兑换信息体
        :param gpt_msg: gpt响应回来的信息
        :param messages: 对话信息体
        :return:
        """
        # 如果返回信息成功，则往长对话内容添加新内容
        if gpt_msg:
            messages += [{"role": "user", "content": gpt_msg}]
        # 返回失败则删除可能造成问题的
        else:
            messages.pop()
        if self.chat_id:
            # todo 保存方案待定
            pass
            # cache[self.chat_id] = messages

    async def ask_openai(self, msg):
        """
        问询主程
        :param msg:
        :return:
        """
        pass


import openai
import asyncio


async def generate_text(input_msg):
    openai.api_key = "sk-x"
    openai.proxy = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }
    # model_engine = "text-davinci-002"
    model_engine = "gpt-3.5-turbo"
    messages = []
    messages += [{"role": "user", "content": input_msg}]
    completions = await openai.ChatCompletion.acreate(
        model=model_engine,
        messages=messages,
        temperature=1
    )
    message = completions['choices'][0]['message']['content']
    return message


async def main():
    prompt = "中午吃什么？"
    message = await generate_text(prompt)
    print(message)


if __name__ == '__main__':
    # asyncio.run(main())
    loop = asyncio.get_event_loop()  # 创建一个事件循环对象loop
    try:
        loop.run_until_complete(main())  # 完成事件循环，直到最后一个任务结束
    finally:
        loop.close()  # 结束事件循环.
