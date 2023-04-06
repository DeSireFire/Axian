#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/29
# CreatTIME : 13:54
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import asyncio
from nonebot.internal.rule import Rule
import nest_asyncio
nest_asyncio.apply()
"""
信息响应主体
"""

from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot import on_message, on_keyword
from nonebot.rule import to_me
from .handlers import msgReply, imgDALLE


# 命令关键词
keyword_comm = {"：：i", "：：I", "::i", "::I", "AGI I", "agi i"}


# Event 信息匹配过滤
async def img_rule(event: Event) -> bool:
    """
    便于日后添加更复杂的过滤逻辑
    :param event:
    :return:
    """
    msg = str(event.get_message())
    for i in list(keyword_comm):
        if msg.startswith(i):
            return True
        else:
            continue
    return False


forwardRule = Rule(img_rule) & to_me()
dalle_img = on_message(rule=forwardRule, priority=998)
@dalle_img.handle()
async def chatCallBack(bot: Bot, event: Event):
    user_msg = str(event.get_message())
    session_id = event.get_session_id()
    event_dict = dict(event)
    mid = event_dict.get("message_id")
    msgs = [
        '收到!奋笔涂鸦ing...',
    ]
    await msgReply(bot, event, msgs)

    obj = imgDALLE()
    obj.chat_id = session_id
    obj.input_clear += list(keyword_comm)
    dealle_img = await obj.ask_openai(user_msg)
    print(obj.api_keys)
    print(dealle_img)
    if "http" in dealle_img:
        msgs = [
            MessageSegment.reply(mid),
            MessageSegment(type='text', data={'text': f"根据 {user_msg} 我完成的涂鸦~"}),
            MessageSegment.image(dealle_img),
        ]
    else:
        msgs = [
            MessageSegment.reply(mid),
            MessageSegment(type='text', data={'text': f"画不出来了..{dealle_img}"}),
        ]

    callback_msg = Message(msgs)

    await dalle_img.finish(callback_msg)


