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

gptHelp = on_keyword({"::help", "::帮助", "：：帮助", "：：help"}, rule=to_me(), priority=1, block=True)
@gptHelp.handle()
async def gptHelpCallBack(bot: Bot, event: Event):
    user_msg = str(event.get_message())
    session_id = event.get_session_id()
    event_dict = dict(event)
    mid = event_dict.get("message_id")
    readme = (
        "::help : 命令帮助\n"
        "::c : chat 聊天模式\n"
        "::i : img 图片模式\n"
        "::f : files 文件模式\n"
        "::a : files 文件模式\n"
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