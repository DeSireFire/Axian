#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/7/20
# CreatTIME : 12:53 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import random
import asyncio
from src.plugins.acrobatics import *
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message
from nonebot.rule import to_me
from nonebot.params import CommandArg

ql_driver = on_keyword({"面包"}, rule=to_me(), priority=1, block=True)


@ql_driver.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    """
    测试获取昵称
    :param event: 事件对象，消息对象
    :param arg: 参数对象，跟随命令的参数
    :return:
    """
    # 提取信息纯文本字符串，并作清洗切割
    user_name = event.sender.card or event.sender.nickname
    if randomCB(5):
        # 向用户回复一条消息（可选），并立即结束当前事件的整个处理流程。
        await ql_driver.finish(f"把那一籃面包推到{user_name}面前")


async def randomCB(probability: int) -> bool:
    """
    概率器，返回真和假
    :param probability: int, 0~9
    :return: bool
    """
    base = list(range(10))
    roll_num = random.choice(base)
    if probability > roll_num:
        return True
    else:
        return False



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
