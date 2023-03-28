#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/28
# CreatTIME : 17:49
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot import on_message, on_keyword
from nonebot.rule import to_me
from nonebot import get_driver

# todo 更详细的触发条件
chatgptDemp = on_keyword({"::help", "::帮助"}, rule=to_me(), priority=1, block=True)
@chatgptDemp.handle()
async def gptHelpCallBack(bot: Bot, event: Event):
    user_msg = str(event.get_message())
    session_id = event.get_session_id()
    event_dict = dict(event)
    mid = event_dict.get("message_id")
    msgs = [
        MessageSegment.reply(mid),
        MessageSegment.text(f'回声：{user_msg}'),
    ]
    callback_msg = Message(msgs)
    await bot.send(
        event=event,
        message=callback_msg
    )