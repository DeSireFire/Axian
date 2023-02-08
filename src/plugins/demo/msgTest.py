#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/10/14
# CreatTIME : 10:56 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot import on_message, on_command
import ast

# 命令接收测试
test = on_command('test')


@test.handle()
async def _(bot: Bot, event: Event):
    # call_api的写法一
    data = await bot.call_api('get_group_info', **{
        'group_id': 813781752
    })
    # 对json进行转义,安全的eval
    data = ast.literal_eval(str(data))
    msg = f"群号  ：{data['group_id']}\
          \n群名称：{data['group_name']}\
          \n成员数：{data['member_count']}"
    # call_api的写法二
    await bot.send(
        event=event,
        message=msg
    )


from nonebot import on_message
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Event

# # 阻断事件练习
# def can_pass(message):
#     # 判断是否可以通过
#     if message=="1":
#         return True
#     else:
#         return False
#
# bot_guard = on_message(priority=1, block=False) # block=False 即默认不阻断事件
# @bot_guard.handle()
# async def bot_guard_handle(matcher: Matcher,event: Event):
#     message = str(event.get_message()) # 获取用户所发的消息内容
#     if not can_pass(message):          # 如果返回值是False则阻断事件
#         matcher.stop_propagation()
#     else:
#         print(f"接收信息： {message}. ")


# # Event 事件测试，检查用户
# async def user_checker(event: Event) -> bool:
#     if event.get_user_id() == "1025212779":
#         print("是master")
#         return True
#     else:
#         print("不是master")
#         return False
#
# setu_sender = on_message(rule=user_checker)

# 测试未成功
from nonebot.permission import SUPERUSER

matcher = on_command("测试超管", permission=SUPERUSER)


@matcher.handle()
async def _(event: Event):
    message = str(event.get_message())
    print(message)
    await matcher.send("超管命令测试成功")

# @matcher.got("key1", "超管提问")
# async def _():
#     await matcher.send("超管命令 got 成功")


# from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN,PRIVATE
# # 这个响应器将会对任意私聊或群聊中的管理员进行响应
# """
# 权限类型	匹配范围
# PRIVATE	全部私聊
# PRIVATE_FRIEND	私聊好友
# PRIVATE_GROUP	群临时私聊
# PRIVATE_OTHER	其他临时私聊
# GROUP	全部群聊
# GROUP_MEMBER	任意群员
# GROUP_ADMIN	群管理
# GROUP_OWNER	群主
# """
# matcher = on_command("setu", permission=PRIVATE|GROUP_ADMIN)
