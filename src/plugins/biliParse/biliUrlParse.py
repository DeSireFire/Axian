#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/11/1
# CreatTIME : 15:30 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import ast
import json
import xmltodict
import requests
from pprint import pprint
from urllib.parse import urlparse
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from src.utils.url_common import urlParam_to_dict
from nonebot import on_message, on_keyword, on_command
from src.components.parseHandlers import jsonPath_detail
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment, GROUP



# biliAppShare = on_message(rule=bvAppShare_checker)
# @biliAppShare.handle()
# async def bvAppShareParse(bot: Bot, event: Event):
#     message = str(event.get_message())  # 获取用户所发的消息内容

# auto_analysis = on_keyword(['BV','bv','bV','Bv','b23.tv'],permission=GROUP,priority=49)
auto_analysis = on_keyword(['BV','bv','bV','Bv','b23.tv'],priority=49)
@auto_analysis.handle()
async def analysis(bot: Bot, mathcer: Matcher, event: GroupMessageEvent):
    """
    群解析测试
    :param bot:
    :param mathcer:
    :param event:
    :return:
    """
    print()
