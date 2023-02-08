#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/2/06
# CreatTIME : 12:53
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import random
import asyncio

from nonebot.internal.rule import Rule
from nonebot.matcher import Matcher
from . import *
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, MessageEvent, GroupMessageEvent
from nonebot.rule import to_me
from nonebot import on_message, on_keyword
from nonebot.params import CommandArg


# 信息转发
detection_group = [681666551, 813781752, 1130724261]
# detection_group = [701568701]
push_group = [758810535, 774150811]
# Event 检测是否为包含图片信息
async def imgMessage(event: Event) -> bool:
    msg_list = list(event.get_message())
    res_bool = False
    # 检测信息类型，包含图片类型的信息就返回真
    for m in msg_list:
        if "image" == m.type:
            # print(f"rula测试-——imgMessage-->:{str(event.get_message())}")
            res_bool = True
            break
    return res_bool

# Event 检测是否为指定监控的群体信息
async def specifyGroupMessage(event: Event) -> bool:
    # 将event转化成字典，方便后面的处理
    event_dict = dict(event)

    # 排除非群信息
    get_session_id = str(event.get_session_id())
    if not get_session_id.startswith('group'):
        return False
    group_id = event_dict.get("group_id")
    if group_id in detection_group:
        # print(f"rula测试-—specifyGroupMessage—-->:{group_id}")
        return True
    else:
        return False

forwardRule = Rule(imgMessage, specifyGroupMessage)
setuGroupForward = on_message(rule=forwardRule)

@setuGroupForward.handle()
async def setuGroupForwardMain(bot: Bot, event: Event, matcher: Matcher):
    event_dict = dict(event)
    raw_dict = {}
    raw_msgs = list(event_dict.get('message'))
    raw_dict["sender"] = event.get_user_id() or "415592997"
    raw_dict["imgs"] = {i.data.get("file"): i.data.get("url") for i in raw_msgs} or {}
    raw_dict["len"] = len(list(raw_dict["imgs"].keys()))
    if not raw_dict["imgs"]:          # 如果返回值是False则阻断事件
        matcher.stop_propagation()

    # 信息装填
    msgs = [
        # MessageSegment(type='text', data={'text': f"啊对对对！"}),
        MessageSegment(type='image', data={'file': v}) for k, v in raw_dict.get('imgs').items() if ".image" in k
    ]
    msgs = await msgs_return_line(msgs)
    callback_msg = Message(msgs)
    await bot.send_group_msg(
        group_id=push_group[0],
        message=callback_msg
    )

async def msgs_return_line(msgs: list) -> list:
    """
    批量在消息对象之间插入换行符
    :param msgs:list,MessageSegment对象
    :return:
    """
    res_msgs = []
    for i, m in enumerate(msgs, start=1):
        # print(f"res_msgs--->{res_msgs}")
        res_msgs.append(m)
        if i == len(msgs):  # 末尾不添加换行
            break
        res_msgs.append(MessageSegment.text("\n"))
    return res_msgs
# 消息撤回
# textRetract = on_message(rule=bvAppShare_checker)
