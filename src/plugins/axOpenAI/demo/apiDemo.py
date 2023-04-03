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
from nonebot import get_driver
from .gptCompose import *

# 设置
nb_config = get_driver().config.dict()
self_name = nb_config.get('nickname', [])

keywords = set([":::", "：：："]+[f"@{i} :::" for i in self_name]+[f"@{i} ：：：" for i in self_name])
chatgptDemp = on_keyword(keywords, rule=to_me(), priority=10, block=True)
@chatgptDemp.handle()
async def chatgptCallBack(bot: Bot, event: Event):
    user_msg = str(event.get_message())
    session_id = event.get_session_id()
    event_dict = dict(event)
    mid = event_dict.get("message_id")
    readme = (
        "::: 命令功能已暂时下限\n"
        "使用以下命令来与bot交互：\n"
        "::help : 命令帮助\n"
    )
    msgs = [
        MessageSegment.reply(mid),
        MessageSegment.text(f'{readme}'),
    ]
    callback_msg = Message(msgs)
    await bot.send(
        event=event,
        message=callback_msg
    )

# keywords = set([":::", "：：："]+[f"@{i} :::" for i in self_name]+[f"@{i} ：：：" for i in self_name])
# chatgptDemp = on_keyword(keywords, rule=to_me(), priority=10, block=True)
# @chatgptDemp.handle()
# async def chatgptCallBack(bot: Bot, event: Event):
#     user_msg = str(event.get_message())
#     session_id = event.get_session_id()
#     mid = event.message_id
#     # 实例化
#     opai = OpenAIOfficial()
#     # 参数设置
#     opai.chat_id = session_id
#     opai.clear_kw = keywords
#     gpt_msg = opai.ask_chatgpt(user_msg)
#     msgs = [
#         MessageSegment.reply(mid),
#         MessageSegment.text(f'{gpt_msg}'),
#     ]
#     callback_msg = Message(msgs)
#     await bot.send(
#         event=event,
#         message=callback_msg
#     )

test = on_keyword({"t2t"}, rule=to_me(), priority=1, block=True)
@test.handle()
async def testCallBack(bot: Bot, event: Event):
    user_msg = str(event.get_message())
    mid = event.message_id
    msgs = [MessageSegment.reply(mid)]

    cache_len = len(list(cache.keys())) or "无"
    cache_keys = list(cache.keys()) or "无"
    cache_dict = {k: len(v) for k, v in cache.items()} or "无"
    msgs += [MessageSegment.text(
        f'cache_len:{cache_len},'
        f'cache_keys:{cache_keys},'
        f'cache_dict:{cache_dict},'
    )]
    callback_msg = Message(msgs)
    await bot.send(
        event=event,
        message=callback_msg
    )
