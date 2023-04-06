#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/4/4
# CreatTIME : 17:27
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

bing_push = on_message(priority=100, permission=GROUP, block=False)
bing_news = []

@bing_push.handle()
async def _bing_push(bot: Bot, event: MessageEvent):
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
        'authority': 'assets.msn.cn',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    }
    urls = [
        'https://assets.msn.cn/service/news/feed/pages/binghp'
    ]
    params = {
        'activityId': '9E2721EA-9DB7-4AB0-8920-183E2FADD190',
        'apikey': 'QMmdky7jrTlM4mWJmMYQTi71lp678KyZJBKHCAyKCg',
        'cm': 'zh-cn',
        'it': 'web',
        'ocid': 'bingHomepage-newsfeed',
        'timeOut': '2000',
        'user': 'm-1E6512A74A1D68D92C28004F4B576970',
        'wpopageid': 'wponoads',
    }
    rdb = RedisSet(1)
    rkey = "Axian:news:bing"
    bing_news = rdb.get_all(rkey) or []
    if not bing_news:
        cls = RequestGet(urls)
        cls.headers = headers
        res = cls.url_get(params=params)
        news = [i.json() for i in res]
        subCards = jsonPath_detail(news, ['subCards']).getall() or []
        bing_news = [i.get('title') for i in subCards if i.get('title')] or []
        # 保存信息信息
        rdb.add_all(rkey, bing_news)
        rdb.expire(rkey, 60*30)
    else:
        if random.choice(list(range(1, 11))) > 8 and event_dict.get("group_id") == 813781752:
            pop_new = "".join(rdb.conn.spop(rkey, 1))
            if pop_new:
                await send_group_message(bot, 813781752, f"{user_name}, 我跟你讲，刚才我看到个新闻，{pop_new}'.你咋看？")

# @bing_push.handle()
# async def _bing_push(bot: Bot, event: MessageEvent):
#     """
#     测试获取昵称
#     :param event: 事件对象，消息对象
#     :param arg: 参数对象，跟随命令的参数
#     :return:
#     """
#     # 提取信息纯文本字符串，并作清洗切割
#     user_name = event.sender.card or event.sender.nickname
#     event_dict = dict(event)
#     # print(event_dict)
#     timestamp = event_dict['time']
#     local_time = time.localtime(timestamp)
#     target_time = (
#         local_time.tm_year, local_time.tm_mon, local_time.tm_mday,
#         11, 30, 0,
#         local_time.tm_wday, local_time.tm_yday, local_time.tm_isdst
#     )
#
#
#
#     headers = {
#         'authority': 'assets.msn.cn',
#         'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
#     }
#     urls = [
#         'https://assets.msn.cn/service/news/feed/pages/binghp'
#     ]
#     params = {
#         'activityId': '9E2721EA-9DB7-4AB0-8920-183E2FADD190',
#         'apikey': 'QMmdky7jrTlM4mWJmMYQTi71lp678KyZJBKHCAyKCg',
#         'cm': 'zh-cn',
#         'it': 'web',
#         'ocid': 'bingHomepage-newsfeed',
#         'timeOut': '2000',
#         'user': 'm-1E6512A74A1D68D92C28004F4B576970',
#         'wpopageid': 'wponoads',
#     }
#     rdb = RedisSet(1)
#     bing_news = rdb.get_all("Axian:bing_news") or []
#     if time.mktime(local_time) > time.mktime(target_time):
#         print('是上午11点半之后')
#
#         cls = RequestGet(urls)
#         cls.headers = headers
#         res = cls.url_get(params=params)
#         news = [i.json() for i in res]
#         subCards = jsonPath_detail(news, ['subCards']).getall() or []
#         bing_news = [i.get('title') for i in subCards if i.get('title')] or []
#         print(bing_news)
#     else:
#         bing_news = []
#         print('是上午11点半之前')

async def send_group_message(bot: Bot, group_id: int, message: str):
    await bot.call_api('send_group_msg', **{
        'group_id': group_id,
        'message': message,
    })
