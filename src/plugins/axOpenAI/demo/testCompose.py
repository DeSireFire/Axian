#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/20
# CreatTIME : 15:51
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import asyncio

import httpx
import openai
import logging
import random
from typing import List

# class ChatGPTClient:
#     def __init__(
#         self,
#         api_keys: List[str],
#         timeout: int = 10,
#         retry_count: int = 3,
#         proxies: dict = None,
#         log_level: str = "INFO",
#     ):
#         self.api_keys = api_keys
#         self.timeout = timeout
#         self.retry_count = retry_count
#         self.proxies = proxies
#         self.log_level = log_level
#         self.logger = logging.getLogger(__name__)
#         self.logger.setLevel(log_level)
#
#     async def _request(
#         self, url: str, headers: dict = None, data: dict = None
#     ) -> dict:
#         async with httpx.AsyncClient(
#             headers=headers,
#             timeout=self.timeout,
#             proxies=self.proxies,
#         ) as client:
#             response = await client.post(url, data=data)
#             if response.status_code != 200:
#                 raise Exception(f"Request failed with status code {response.status_code}")
#             return response.json()
#
#     async def _retry_request(
#         self, url: str, headers: dict = None, data: dict = None
#     ) -> dict:
#         for i in range(self.retry_count):
#             try:
#                 response = await self._request(url, headers=headers, data=data)
#                 return response
#             except Exception as e:
#                 self.logger.warning(f"Request failed with error: {e}")
#         raise Exception("Request failed after retrying")
#
#     async def send_message(self, message: str) -> str:
#         url = "https://api.chatgpt.com/message"
#         headers = {"Authorization": f"Bearer {self.api_keys[0]}"}
#         data = {"message": message}
#         response = await self._retry_request(url, headers=headers, data=data)
#         return response["message"]
#
# if __name__ == "__main__":
#     api_keys = ["api_key_1", "api_key_2"]
#     client = ChatGPTClient(api_keys=api_keys)
#
#     async def test_send_message():
#         message = "Hello, how are you?"
#         response = await client.send_message(message)
#         print(response)
#
#     asyncio.run(test_send_message())




class ChatGPT:
    def __init__(self, api_keys: List[str], timeout: int = 10, retries: int = 3, proxies: dict = None):
        self.api_keys = api_keys
        self.timeout = timeout
        self.retries = retries
        self.proxies = proxies
        self.log = logging.getLogger(__name__)

    async def _request(self, prompt: str, api_key: str):
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {api_key}"}
        data = {"prompt": prompt, "temperature": 0.7, "max_tokens": 150}
        async with httpx.AsyncClient(timeout=self.timeout, proxies=self.proxies) as client:
            response = await client.post("https://api.openai.com/v1/engines/davinci-codex/completions", headers=headers, json=data)
            if response.status_code == 200:
                return response.json()["choices"][0]["text"]
            else:
                self.log.error(f"Request failed with status code {response.status_code}")
                return None

    async def _retry_request(self, prompt: str):
        for i in range(self.retries):
            api_key = random.choice(self.api_keys)
            response = await self._request(prompt, api_key)
            if response:
                return response
        self.log.error("All retries failed")
        return None

    async def send_message(self, prompt: str):
        response = await self._retry_request(prompt)
        if response:
            self.log.info(f"Received response: {response}")
            return response
        else:
            self.log.error("Failed to get response")
            return None

if __name__ == "__main__":
    openai.api_key = "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"
    chatbot = ChatGPT(api_keys=[openai.api_key], timeout=10, retries=3, proxies=None)
    prompt = "今晚吃什么?"
    response = await chatbot.send_message(prompt)
    if response:
        print(response)
    else:
        print("Failed to get response")