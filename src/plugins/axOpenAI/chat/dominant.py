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
ckeyword_comm = {"：：c", "：：C", "::c", "::C", "AGI C", "agi c"}
pkeyword_comm = {"：：p", "：：P", "::p", "::P", "AGI P", "agi p"}

# Event 信息匹配过滤
async def cchat_rule(event: Event) -> bool:
    """
    便于日后添加更复杂的过滤逻辑
    :param event:
    :return:
    """
    msg = str(event.get_message())
    for i in list(ckeyword_comm):
        if msg.startswith(i):
            return True
        else:
            continue
    return False

# Event 信息匹配过滤
async def pchat_rule(event: Event) -> bool:
    """
    便于日后添加更复杂的过滤逻辑
    :param event:
    :return:
    """
    msg = str(event.get_message())
    for i in list(pkeyword_comm):
        if msg.startswith(i):
            return True
        else:
            continue
    return False


chain_chat_Rule = Rule(cchat_rule) & to_me()
prompt_chat_Rule = Rule(pchat_rule) & to_me()
chain_chat = on_message(rule=chain_chat_Rule, priority=998)
prompt_chat = on_message(rule=prompt_chat_Rule, priority=998)

# 记忆上下文
@chain_chat.handle()
async def cchatCallBack(bot: Bot, event: Event):
    user_msg = str(event.get_message())
    session_id = event.get_session_id()
    event_dict = dict(event)
    mid = event_dict.get("message_id")
    # 回声回复，先给用户正向反馈
    loading_msg = [
        MessageSegment.reply(mid),
        MessageSegment.text(f'emmm...')
    ]
    await bot.send(
        event=event,
        message=Message(loading_msg)
    )

    # 获取gpt内容
    obj = chatgpt()
    obj.chat_id = session_id
    obj.input_clear += list(ckeyword_comm)
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

# 不记忆上下文
@prompt_chat.handle()
async def schatCallBack(bot: Bot, event: Event):
    user_msg = str(event.get_message())
    session_id = event.get_session_id()
    event_dict = dict(event)
    mid = event_dict.get("message_id")
    # 回声回复，先给用户正向反馈
    loading_msg = [
        MessageSegment.reply(mid),
        MessageSegment.text(f'emmm...')
    ]
    await bot.send(
        event=event,
        message=Message(loading_msg)
    )

    # 获取gpt内容
    obj = chatgpt()
    obj.chat_id = None
    obj.input_clear += list(pkeyword_comm)
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
