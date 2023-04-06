#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/4/3
# CreatTIME : 14:30
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment


async def msgReply(bot, event, messages):
    """
    消息回复
    :param bot: bot对象
    :param event: event对象
    :param messages: list, 回复信息列表，每个元素一行
    :return:
    """
    event_dict = dict(event)
    mid = event_dict.get("message_id")
    msgs = [
        MessageSegment.reply(mid),

    ]
    for i, m in enumerate(messages, start=1):
        if i != len(messages):
            msgs.append(MessageSegment.text(f'{m}\n'))
        else:
            msgs.append(MessageSegment.text(f'{m}'))
    callback_msg = Message(msgs)
    await bot.send(
        event=event,
        message=callback_msg
    )
