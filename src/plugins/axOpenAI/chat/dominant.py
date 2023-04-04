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
from .handlers import chatgpt

# 命令关键词
keyword_comm = {"：：c", "：：C", "::c", "::C", "AGI C", "agi c"}


# Event 信息匹配过滤
async def chat_rule(event: Event) -> bool:
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


forwardRule = Rule(chat_rule) & to_me()
gpt_chat = on_message(rule=forwardRule, priority=998)

@gpt_chat.handle()
async def chatCallBack(bot: Bot, event: Event):
    user_msg = str(event.get_message())
    session_id = event.get_session_id()
    event_dict = dict(event)
    mid = event_dict.get("message_id")
    obj = chatgpt()
    obj.chat_id = session_id
    obj.input_clear += list(keyword_comm)
    gpt_msg = await obj.ask_openai(user_msg)
    msgs = [
        MessageSegment.reply(mid),
    ]
    msgs += [
        MessageSegment.text(f'{gpt_msg}')
    ]
    callback_msg = Message(msgs)
    await bot.send(
        event=event,
        message=callback_msg
    )

    # gpt_msg_list = gpt_msg.split("\n") or []
    # gpt_msg_list = [i.strip() for i in gpt_msg_list if i or i.strip()]
    # for line in gpt_msg_list:
    #     lmsgs = [
    #         MessageSegment.reply(mid),
    #         MessageSegment.text(f'{line}'),
    #     ]
    #     callback_msg = Message(lmsgs)
    #     await bot.send(
    #         event=event,
    #         message=callback_msg
    #     )
    #     await asyncio.sleep(1)



# gpt_test = on_message(rule=to_me(), priority=999)
# @gpt_test.handle()
# async def testCallBack(bot: Bot, event: Event):
#     user_msg = str(event.get_message())
#     session_id = event.get_session_id()
#     event_dict = dict(event)
#     mid = event_dict.get("message_id")
#     msgs = [
#         MessageSegment.reply(mid),
#         MessageSegment.text(f'\nuser_msg:{user_msg}'),
#         MessageSegment.text(f'\nsession_id:{session_id}'),
#         MessageSegment.text(f'\nmid:{mid}'),
#     ]
#     callback_msg = Message(msgs)
#     # await gpt_chat.finish()
#     # await bot.can_send_image()
#     await bot.send(
#         event=event,
#         message=callback_msg
#     )
