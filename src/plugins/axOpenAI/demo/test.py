#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/24
# CreatTIME : 16:16
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import thulac

thu = thulac.thulac() #默认模式
text = "获取全世界国家和地区，及其谐音词，常用代指词整合成python列表"
result = thu.cut(text, text=False)  # 进行一句话分词
print(dict(result))
clear_list = [k for k, v in dict(result).items() if v in ["w", "c", "r"]]
for i in clear_list:
    text = text.replace(i, " ")
print(text)