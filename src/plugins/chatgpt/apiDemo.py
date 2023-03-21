#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/20
# CreatTIME : 15:21
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot import on_message, on_keyword
from nonebot.rule import to_me
from .gptCompose import *

chatgptDemp = on_keyword({"cgpt"}, rule=to_me(), priority=1, block=True)
@chatgptDemp.handle()
async def chatgptCallBack(bot: Bot, event: Event):
    user_msg = str(event.get_message())
    opai = OpenAIOfficial([])
    gpt_msg = opai.askChatGPT(user_msg)
    msgs = [MessageSegment.text(f'{gpt_msg}')]
    callback_msg = Message(msgs)
    await bot.send(
        event=event,
        message=callback_msg
    )
