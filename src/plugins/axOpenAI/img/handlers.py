#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/29
# CreatTIME : 13:53
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import random

import openai
import asyncio
from ..utils import setting_api_key, setting_proxies
from ..components.OpenAI import OpenAIBase
from ..components.MsgCallback import msgReply

class imgDALLE(OpenAIBase):
    def __init__(self):
        super().__init__()
        self.model = ""

    async def ask_openai(self, input_msg):
        # 清洗信息
        imsg = await self.input_message_clear(input_msg)

        # 获取&构造对话信息
        # chats = await self.structure_chat(imsg)

        # 获取gpt响应信息
        try:
            gpt_msg = await self.generate_img(imsg)
        except Exception as oe:
            self.log.error(f"openai报错啦！{oe}")
            gpt_msg = random.choice(self.reply_ban_answer)

        # 更新&保存对话信息
        # u2s = await self.update_to_save_chat(imsg, gpt_msg)

        return gpt_msg

