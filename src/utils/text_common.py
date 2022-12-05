#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/10/17
# CreatTIME : 15:53 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import re
def re_getall(html_text, re_pattern, nbsp_del=True):
    '''
    正则过滤函数
    :param html_text: 字符串，网页的文本
    :param re_pattern: 字符串，正则表达式
    :param nbsp_del: 布尔值，控制是否以去除换行符的形式抓取有用信息
    :return:
    '''
    pattern = re.compile(re_pattern)
    if nbsp_del:
        return pattern.findall("".join(html_text.split()))
    else:
        return pattern.findall(html_text)