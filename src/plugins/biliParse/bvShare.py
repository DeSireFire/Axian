#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/10/17
# CreatTIME : 10:46 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

from pprint import pprint
from urllib.parse import urlparse
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageSegment
from nonebot import on_message, on_keyword
from src.components.parseHandlers import jsonPath_detail
from src.utils.url_common import urlParam_to_dict
import ast
import json
import xmltodict
import requests

"""
检测到B站app分享的视频是自动解析视频内容
"""


# Event 检测是否未blapp
async def bvAppShare_checker(event: Event) -> bool:
    msg = str(event.get_message())
    # print(f"rula测试--->:{str(event.get_message())}")
    if "CQ:xml" in msg and 'name="哔哩哔哩"' in msg:
        return True
    elif "CQ:json" in msg and '哔哩哔哩' in msg and 'source_icon' in msg:
        return True
    else:
        return False


biliAppShare = on_message(rule=bvAppShare_checker)


@biliAppShare.handle()
async def bvAppShareParse(bot: Bot, event: Event):
    message = str(event.get_message())  # 获取用户所发的消息内容
    raw_dict = {}
    if "CQ:xml" in message:
        xml_str = await get_cq_xml_data(message)
        raw_dict = xmltodict.parse(xml_str)
    if "CQ:json" in message:
        json_str = await get_cq_json_data(message)
        raw_dict = json.loads(json_str)
    summary = jsonPath_detail(raw_dict, ['summary']).get() or None
    cover = jsonPath_detail(raw_dict, ['@cover']).get() or None
    bvUrl = jsonPath_detail(raw_dict, ['@url']).get() or None
    bvDict = await get_url_dict(bvUrl) if bvUrl else {}
    msgs = [
        MessageSegment(type='image', data={'file': cover}),
        MessageSegment(type='text', data={'text': f"{summary}"}),
    ]
    pprint(bvDict)
    if bvDict and bvDict.get("url"):
        # callback_msg += MessageSegment.text(f"视频传送门:https://www.bilibili.com/video/{summary}")
        msgs += [MessageSegment.text(f'视频传送门:{bvDict.get("url")}')]
    msgs = await msgs_return_line(msgs)
    callback_msg = Message(msgs)
    await bot.send(
        event=event,
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


async def get_cq_xml_data(cq_str: str) -> str:
    """
    获取cq信息中的data字符串
    [CQ:xml,data=<?xml version='1.0' encoding='UTF-8' standalone='yes'?><msg templateID="123" url="https://b23.tv/ka7iXdX?share_medium=android&amp;amp;share_source=qq&amp;amp;bbid=XX0D99D01758D3381DC0E83A4F395A8B1A3D4&amp;amp;ts=1665978517942" serviceID="1" action="web" actionData="" a_actionData="" i_actionData="" brief="&#91;QQ小程序&#93;哔哩哔哩" flag="0"><item layout="2"><picture cover="http://pubminishare-30161.picsz.qpic.cn/5b2c43f6-606e-46a8-b6e7-ead20fc47ab5"/><title>哔哩哔哩</title>...></msg>,resid=]
    :param cq_str:
    :return:
    """
    split_start = ",data="
    split_end = ",resid="
    res = cq_str[cq_str.find(split_start) + len(split_start):cq_str.find(split_end)] or ""
    return res


async def get_cq_json_data(cq_str: str) -> str:
    """
    获取cq信息中的data字符串
    [CQ:json,data={ "app": "com.tencent.structmsg"&#44; "config": { "ctime": 1665996173&#44; "forward": true&#44; "token": "9c4874848d1002371f2641316e420915"&#44; "type": "normal" }&#44; "desc": "新闻"&#44; "meta": { "news": { "action": ""&#44; "android_pkg_name": ""&#44; "app_type": 1&#44; "appid": 100951776&#44; "ctime": 1665996173&#44; "desc": "《機動戰士鋼彈 水星的魔女（僅限港澳台地區）》鋼彈系列最新作品"&#44; "jumpUrl": "https:\/\/b23.tv\/5w9xAfh?share_medium=android&amp;share_source=qq&amp;bbid=XU373453E73D7EFC5712DCE61D838CD157134&amp;ts=1665996166235"&#44; "preview": "https:\/\/pic.ugcimg.cn\/df700efa0439332c69823d3dfec5dc2a\/jpg1"&#44; "source_icon": "https:\/\/open.gtimg.cn\/open\/app_icon\/00\/95\/17\/76\/100951776_100_m.png?t=1659061321"&#44; "source_url": ""&#44; "tag": "哔哩哔哩"&#44; "title": "《機動戰士鋼彈 水星的魔女（僅限港澳台地區）》 第3话 古.…"&#44; "uin": 1632436845 } }&#44; "prompt": "&#91;分享&#93;《機動戰士鋼彈 水星的魔女（僅限港澳台地區）》 第3话 古.…"&#44; "ver": "0.0.0.1"&#44; "view": "news" }]
    :param cq_str:
    :return:
    """
    split_start = ",data="
    split_end = "}]"
    res = cq_str[cq_str.find(split_start) + len(split_start):cq_str.find(split_end) + 1] or ""
    return res


async def get_url_dict(bl_url: str) -> dict:
    """
    从url当中获取参数信息
    :param bl_url: str,bili的分享链接
    :return:
    """
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7,und;q=0.6,ja;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-platform': '"Windows"',
    }
    response = requests.get(bl_url, headers=headers)
    rurl = urlparse(response.url)
    res_dict = urlParam_to_dict(response.url) or {}
    res_dict["raw_url"] = response.url
    res_dict["url"] = f"{rurl.scheme}://{rurl.netloc}{rurl.path}"
    return res_dict


if __name__ == '__main__':
    bvUrl = ""
    temp = get_url_dict(bvUrl)
