#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/7/10
# CreatTIME : 16:04 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from nonebot import on_command
from nonebot.params import RawCommand

matcher = on_command("test", aliases={"test", "test"}, priority=5, block=True)

@matcher.handle()
async def _(event: str = RawCommand()):
    await matcher.send("Hello world!")


# @matcher.handle()
# async def _():
#     """
#     向用户回复一条消息。回复的方式或途径由协议适配器自行实现。
#
#     可以是 str、Message、MessageSegment 或 MessageTemplate。
#
#     这个操作等同于使用 bot.send(event, message, **kwargs) 但不需要自行传入 event。
#     :return:
#     """
#     await matcher.send("Hello world!")

# @matcher.handle()
# async def _():
#     """
#     向用户回复一条消息（可选），并立即结束当前事件的整个处理流程。
#     :return:
#     """
#     await matcher.finish("finish Hello world!")