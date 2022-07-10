#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/7/10
# CreatTIME : 16:04 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from nonebot import on_message

matcher = on_message()

@matcher.handle()
async def _():
    await matcher.send("Hello world!")