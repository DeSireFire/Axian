#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/7/15
# CreatTIME : 17:02 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
import random
import asyncio
from . import *
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg

ql_driver = on_command(base_cmd, aliases=base_aliases, priority=5, block=True)

@ql_driver.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    """
    help
    :param event: 事件对象，消息对象
    :param arg: 参数对象，跟随命令的参数
    :return:
    """
    # 提取信息纯文本字符串，并作清洗切割
    msg = arg.extract_plain_text().strip().split() or []
    if not msg:
        # 向用户回复一条消息（可选），并立即结束当前事件的整个处理流程。
        await ql_driver.finish(f"测试msg：{msg}")
    user_name = event.sender.card or event.sender.nickname