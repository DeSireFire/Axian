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
from . import detection_group, push_group
from nonebot.internal.rule import Rule
from nonebot.matcher import Matcher
from src.plugins.acrobatics import *
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, MessageEvent, GroupMessageEvent
from nonebot.rule import to_me
from nonebot import on_message, on_keyword
from nonebot.params import CommandArg
from src.components.netHandlers import RequestHead
from src.components.fileHandlers import bytes_format_detail

"""
信息转发
"""

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
    """
    subTyper
    0	正常图片
    1	表情包, 在客户端会被分类到表情包图片并缩放显示
    2	热图
    3	斗图
    4	智图?
    7	贴图
    8	自拍
    9	贴图广告?
    10	有待测试
    13	热搜图

    :param bot:
    :param event:
    :param matcher:
    :return:
    """
    event_dict = dict(event)
    raw_dict = {}
    raw_msgs = list(event_dict.get('message'))
    # raw_dict["sender"] = event.get_user_id() or "415592997"
    # raw_dict["imgs"] = {i.data.get("file"): i.data.get("url") for i in raw_msgs if i.data.get('subType') == '0'} or {}
    # raw_dict["len"] = len(list(raw_dict["imgs"].keys()))

    # 批量过滤图片
    # cq类型过滤
    temp_imgs = [i.data.get("url") for i in raw_msgs if i.data.get('subType') in ['0', '8', '2', '13']]
    # 条件过滤
    imgs = await img_head_filter(temp_imgs)

    # 未获取到subType=0 的图片时则不执行转发
    # if raw_dict["imgs"]:
    if imgs:
        # 信息装填
        msgs = [
            # MessageSegment(type='text', data={'text': f"啊对对对！"}),
            MessageSegment(type='image', data={'file': url}) for url in imgs
        ]
        msgs = await msgs_return_line(msgs)
        callback_msg = Message(msgs)
        await bot.send_group_msg(
            group_id=push_group[0],
            message=callback_msg
        )


# 工具函数
async def img_head_filter(img_urls: list) -> list:
    """
    过滤干扰图片
    img_urls：
    {"xxx.image":url,...}
    :param img_urls: dict, 需要过滤图片url
    :return: img_urls, 通过过滤的url
    """
    if not img_urls:
        return []

    cls = RequestHead(img_urls)
    responses = await cls.async_url_get()

    res_imgs = []
    for r in responses:
        head = dict(r.headers) or {}
        content_len = int(head.get("content-length")) or 0
        _len = bytes_format_detail(content_len)
        # 筛选条件，全真为真
        filter_list = [
            content_len > 100 * 1024,   # 大于100KB大小
        ]
        print(f"url: {str(r.url)}, len:{content_len}, file_size:{_len}")
        if all(filter_list):
            print(f"url: {str(r.url)}, len:{content_len}, file_size:{_len}, 符合过滤需求！")
            res_imgs.append(str(r.url))
    return res_imgs


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
