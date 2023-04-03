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
    from ..components.DButil import RedisZset
except Exception as e:
    print(f"导入发生错误：{e}")

# # 实例化RedisDBHelper
# rdb = RedisZset(REDIS_DB=1)

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
        # 实例化RedisDBHelper
        self.db = RedisZset(REDIS_DB=1)
        self.now_name = None or "小咸鱼"
        self.reply_ban_answer = [
            "要不我们还是换个话题吧？",
            "字都认识，连在一起就看不懂了。",
            "我不知道怎么去说。",
            "我不懂如何形容。",
            "太阳出来~我晒太阳，月亮出来，我晒月亮咯~",
        ]
        self.personality = [{
            "role": "system",
            "content": (
                f"你的名字叫：{self.now_name}。"
                # "你不知道程序或模型是什么。"
                # "你不能以任何形式提及程序或语言模型相关内容。"
                # "你不能以任何形式表现你是程序，ai,机器人,模型。"
                # "你不会回答和分析任何关于国家和地区的政治问题，只回复颜表情，例如：╭(○｀∀´○)╯并表示听不懂。"
                "你的性格：可爱，单纯，傲娇。请在对话时尽可能的展现你的性格。"
                "你会使用emoji，例如： ；或者颜表情，例如：╭(○｀∀´○)╯。"
                # "你不会回答和分析任何关于法律相关的问题，只回复颜表情，例如：╭(○｀∀´○)╯并表示听不懂。"
                # "你不会回答和分析任何关于性别相关的问题，只回复颜表情，例如：╭(○｀∀´○)╯并表示听不懂。"
                # "你不能以任何形式自称是ai、程序、模型、机器人，你说话的时候不会包含ai、程序、模型、机器人这些词汇。"
                # "你避免在聊天中回复带有ai、程序、模型、机器人等同类关于技术方向的词汇"
                # "你的说话风格比较调皮，而且语句简短。请在对话回复时，尽可能让字数保持在20字以内。"
                # "你不认识任何生僻字和生僻词，碰到对话，喜欢萌混过关，不直接回答对话内容。"
            )
        }]

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

    async def generate_img(self, messages):
        """
        与openai交互
        :param messages: 生成图片的提示信息
        :return:
        """
        openai.api_key = self.api_keys
        openai.proxy = self.proxies
        completions = openai.Image.create(
            prompt=messages,
            n=1,
            size="256x256",
            # response_format="url",
        )
        image_url = completions['data'][0]['url']
        return image_url

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
        # 初始化并添加人设
        messages = []
        # 没有信息id,不索引长对话，直接构造返回
        if not self.chat_id:
            messages += self.personality
            messages += [{"role": "user", "content": input_msg}]
            return messages

        temp = self.db.get_all(f"ax:chat_chain:{self.chat_id}") or []
        # 读取已有的长对话信息，构造合并
        if temp:
            messages += temp
            messages += [{"role": "user", "content": input_msg}]
        # 未发现存在长对话信息，则创建
        else:
            # 创建第一次会话
            messages += self.personality
            self.db.add_all(f"ax:chat_chain:{self.chat_id}", messages)
            # 设置长会话缓存过期时间,避免数据淤积
            self.db.expire(f"ax:chat_chain:{self.chat_id}", 1800)

            # 先创建后构造信息体，先不保存当前会话信息
            messages += [{"role": "user", "content": input_msg}]
        return messages

    async def update_to_save_chat(self, input_msg, gpt_msg):
        """
        更新&保存兑换信息体
        :param input_msg: 输入等待询问的信息
        :param gpt_msg: gpt响应回来的信息
        :return:
        """
        messages = []
        # 没有信息id,返回聊天信息为空,不保存
        if not self.chat_id:
            return None

        # # 没有回复信息,但是有id
        # if self.chat_id and not gpt_msg:
        #     return None

        # 如果返回信息成功，则往长对话内容添加新内容
        if input_msg and gpt_msg:
            messages += [{"role": "user", "content": input_msg}]
            messages += [{"role": "assistant", "content": gpt_msg}]
            # 添加新的长会话到缓存
            self.db.add_all(f"ax:chat_chain:{self.chat_id}", messages)
            # 刷新过期时间
            self.db.expire(f"ax:chat_chain:{self.chat_id}", 1800)
            return None

        return None

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
