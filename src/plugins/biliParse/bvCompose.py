#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2022/10/31
# CreatTIME : 17:36 
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
import asyncio
import httpx
import re
from src.utils.url_common import urlParam_to_dict, dict_to_urlParam

class b23Parse(object):
    """
    b23短链接解析
    """
    def __init__(self, b23Url=None):
        assert isinstance(b23Url, str) and "b23" in b23Url, "传入的b23链接参数不正确！"
        self.b23_raw_url = b23Url
        self.re_str = "av(\d{1,12})|BV(1[A-Za-z0-9]{2}4.1.7[A-Za-z0-9]{2})|b23.tv"
        self.bstat_api = "https://api.bilibili.com/x/web-interface/archive/stat"
        self.headers = {
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
        self.bvid = asyncio.run(self.get_bvid) or None
        self.aid = asyncio.run(self.get_aid) or None

    @property
    async def get_bvid(self):
        b23_url = await self.b23_extract(self.b23_raw_url)
        p = re.compile(r"av(\d{1,12})|BV(1[A-Za-z0-9]{2}4.1.7[A-Za-z0-9]{2})")
        video_number = p.search(b23_url)
        bvid = video_number.group() if video_number else None
        return bvid

    @property
    async def get_aid(self):
        if not self.bvid:
            self.bvid = asyncio.run(self.get_bvid)
        assert self.bvid, "获取bvid失败！"
        aid = await self.aid_extract(self.bvid)
        return aid

    async def b23_extract(self, text):
        """
        b23链接，解析跳转地址
        :param text:
        :return:
        """
        b23 = re.compile(r"b23.tv\\/(\w+)").search(text)
        url = ""
        if not b23:
            b23 = re.compile(r"b23.tv/(\w+)").search(text)
        try:
            assert b23 is not None
            b23_number = b23.groups()[0]
            url = f"https://b23.tv/{b23_number}"
        except AssertionError:
            print(f"b23链接解析出错了！")
        resp = httpx.head(url, follow_redirects=True)
        r = str(resp.url)
        return r

    async def aid_extract(self, bvid:str):
        """
        通过bvid获取aid
        :param url: 拼接的
        :return:
        """
        "https://api.bilibili.com/x/web-interface/archive/stat?bvid=BV17x411w7KC"
        'https://api.bilibili.com/x/web-interface/archive/stat?bvid=BV1QF411h7EK'
        url = f"{self.bstat_api}?bvid={bvid}"
        resp = httpx.get(url, headers=self.headers)
        resp_json = resp.json()
        assert resp_json.get("code") == 0,f"解析aid时，发生错误！接口响应明细:{resp_json}"
        return resp_json.get("data").get("aid")

class biliVideoParse(object):
    def __init__(self):
        self.vinfo_api = "https://api.bilibili.com/x/web-interface/view/detail"
        self.vstat_api = "http://api.bilibili.com/x/web-interface/archive/stat"
        self.b23_url = None
        self.aid = None
        self.bvid = None
        self.headers = {
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

    @property
    def video_info_param(self):
        """
        获取基础信息
        服务于self.video_info_api
        :return:
        """
        param = {}
        if self.aid:
            param["aid"] = self.aid
        if not self.aid and self.bvid:
            param["bvid"] = self.bvid
        return param

    def video_stat_param(self):
        """
        获取各类状态信息
        服务于video_stat_api
        :return:
        """
        pass

    async def make_get_request(self, url:str, headers:dict, params=None):
        html = ""
        headers = headers if headers else self.headers
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, params=params)
            assert resp.status_code == 200
            html = resp.text
        return html

if __name__ == '__main__':
    b23s = [
        "https://b23.tv/BV1QF411h7EK",
        "https://b23.tv/kpLP9MF",
    ]
    for u in b23s:
        obj = b23Parse(u)
        print(obj.aid)
        print(obj.bvid)