#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/2/9
# CreatTIME : 10:01
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import requests
import asyncio
import httpx
import time


class NetRequest(object):
    """
    基础请求器
    批量请求链接，批量返回结果
    """

    def __init__(self, urls: list):
        self.headers = {
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'accept': '*/*',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-dest': 'script',
            'accept-language': 'zh-CN,zh-TW;q=0.9,zh;q=0.8,en;q=0.7,und;q=0.6,ja;q=0.5',
        }
        self.urls = urls
        self.method = "GET"

    def url_get(self):
        responses = asyncio.run(self.make_requests())
        return responses

    async def request(self, url, **kwargs):
        async with httpx.AsyncClient() as client:
            resp = await client.request(url=url, method=self.method, headers=self.headers, **kwargs)
            assert resp.status_code == 200
            return resp

    async def make_requests(self, **kwargs):
        tasks = [asyncio.create_task(self.request(_, **kwargs)) for _ in self.urls]
        responses = await asyncio.gather(*tasks)
        return responses


class RequestHead(NetRequest):
    """
    HEAD请求器
    """

    async def async_url_get(self):
        """
        异步函数中调用该方法
        :return:
        """
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.method = "head"
        responses = await self.make_requests()
        return responses

    def url_get(self):
        """
        在同步函数调用该方法
        :return:
        """
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.method = "head"
        responses = asyncio.run(self.make_requests())
        return responses


class RequestGet(NetRequest):
    """
    get请求器
    """

    async def async_url_get(self):
        """
        异步函数中调用该方法
        :return:
        """
        self.method = "get"
        responses = await self.make_requests()
        return responses

    def url_get(self, **kwargs):
        """
        在同步函数调用该方法
        :return:
        """
        self.method = "get"
        responses = asyncio.run(self.make_requests(**kwargs))
        return responses


if __name__ == '__main__':
    urls = [
        # "https://gchat.qpic.cn/gchatpic_new/260229253/1130724261-2969286274-E877E49962108D110E4F171341545FBB/0?term=255&amp;is_origin=0"
        # "https://oaidalleapiprodscus.blob.core.windows.net/private/org-AAWiWvnioiinLwdXfMl7Amw7/user-VC461I6brih2JDhOuQe20WnQ/img-a4YJrIvJDfXGKmVSkVbArazH.png?st=2023-04-07T08%3A27%3A22Z&se=2023-04-07T10%3A27%3A22Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-04-06T20%3A44%3A15Z&ske=2023-04-07T20%3A44%3A15Z&sks=b&skv=2021-08-06&sig=7Wbq7Q8Ep6B6PL0Cpvel0HbOkHCAw8N4ZzcxWntNSqY%3D"
        "https://oaidalleapiprodscus.blob.core.windows.net/private/org-AAWiWvnioiinLwdXfMl7Amw7/user-VC461I6brih2JDhOuQe20WnQ/img-ukNGC9adH9i03wHL40AjtvgL.png?st=2023-04-07T07%3A18%3A37Z&amp;se=2023-04-07T09%3A18%3A37Z&amp;sp=r&amp;sv=2021-08-06&amp;sr=b&amp;rscd=inline&amp;rsct=image/png&amp;skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&amp;sktid=a48cca56-e6da-484e-a814-9c849652bcb3&amp;skt=2023-04-06T20%3A45%3A07Z&amp;ske=2023-04-07T20%3A45%3A07Z&amp;sks=b&amp;skv=2021-08-06&amp;sig=vKRb45cGoEqDNVsuRCJ0KuAT7XaweiV%2Bvn1anmWl5wI%3D,type=,cache=true,proxy=true,timeout="
    ]
    cls = RequestHead(urls)
    res = cls.url_get()
    heads = [dict(i.headers) for i in res]
    print(heads)


