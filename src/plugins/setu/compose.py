#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2023/3/27
# CreatTIME : 15:40
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'
import aiohttp
import asyncio
import os


async def download_file(url, file_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(file_path, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
            else:
                print(f"Failed to download file from {url}")


async def download_with_resume(url, file_path):
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        headers = {'Range': f'bytes={file_size}-'}
    else:
        headers = None
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200 or response.status == 206:
                with open(file_path, 'ab') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
            else:
                print(f"Failed to download file from {url}")


async def main():
    url = 'https://example.com/image.jpg'
    file_path = 'image.jpg'
    await download_file(url, file_path)

    url = 'https://example.com/video.mp4'
    file_path = 'video.mp4'
    await download_with_resume(url, file_path)

if __name__ == '__main__':
    asyncio.run(main())
