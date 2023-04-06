#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/4/6
# CreatTIME : 14:51
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import time
import random

from src.components.netHandlers import RequestGet
from nonebot import on_keyword
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Message, GROUP
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot import on_message, on_keyword
from nonebot.rule import to_me

from src.components.parseHandlers import jsonPath_detail
from src.plugins.acrobatics.compose import RedisSet

bili_push = on_message(priority=100, permission=GROUP, block=False)

@bili_push.handle()
async def _bili_push(bot: Bot, event: MessageEvent):
    """
    测试获取昵称
    :param event: 事件对象，消息对象
    :param arg: 参数对象，跟随命令的参数
    :return:
    """
    # 提取信息纯文本字符串，并作清洗切割
    user_name = event.sender.card or event.sender.nickname
    event_dict = dict(event)
    # print(event_dict)
    headers = {
        'authority': 'app.bilibili.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7,und;q=0.6,ja;q=0.5',
        'origin': 'https://www.bilibili.com',
        'referer': 'https://www.bilibili.com/blackboard/activity-trending-topic.html?navhide=1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    urls = [
        'https://app.bilibili.com/x/v2/search/trending/ranking'
    ]
    params = {
        'limit': '30',
    }
    rdb = RedisSet(1)
    rkey = "Axian:news:bili"
    raw_news = rdb.get_all(rkey) or []
    if not raw_news:
        cls = RequestGet(urls)
        cls.headers = headers
        res = cls.url_get(params=params)
        raw = [i.json() for i in res]
        news = jsonPath_detail(raw, ['show_name']).getall() or []
        # 保存信息信息
        rdb.add_all(rkey, news)
        rdb.expire(rkey, 60*30)
    else:
        if random.choice(list(range(1, 11))) > 8 and event_dict.get("group_id") == 813781752:
            pop_new = "".join(rdb.conn.spop(rkey, 1))
            if pop_new:
                await send_group_message(bot, 813781752, f"{user_name}, 我跟你讲，刚才我看到个新闻，'{pop_new}'.你咋看？")


async def send_group_message(bot: Bot, group_id: int, message: str):
    await bili_push.finish('send_group_msg', **{
        'group_id': group_id,
        'message': message,
    })