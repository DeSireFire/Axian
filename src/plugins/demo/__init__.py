#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/7/10
# CreatTIME : 12:27 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
"""
on: 创建任何类型的事件响应器。
on_metaevent: 创建元事件响应器。
on_message: 创建消息事件响应器。
on_request: 创建请求事件响应器。
on_notice: 创建通知事件响应器。
on_startswith: 创建消息开头匹配事件响应器。
on_endswith: 创建消息结尾匹配事件响应器。
on_fullmatch: 创建消息完全匹配事件响应器。
on_keyword: 创建消息关键词匹配事件响应器。
on_command: 创建命令消息事件响应器。
on_shell_command: 创建 shell 命令消息事件响应器。
on_regex: 创建正则表达式匹配事件响应器。
CommandGroup: 创建具有共同命令名称前缀的命令组。
MatcherGroup: 创建具有共同参数的响应器组。
"""
from . import test