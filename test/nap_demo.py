#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author    : RaXianch
# CreatDATE : 2024/10/31
# CreatTIME : 14:58
# Blog      : https://blog.raxianch.moe/
# Github    : https://github.com/DeSireFire
__author__ = 'RaXianch'

import json
import time
import emoji
import requests
import unicodedata
from pprint import pprint
from collections import Counter
from src.utils.RedisDBHelper import RedisDBHelper
from src.utils.MysqlPool import MysqlPool
from datetime import datetime, timedelta

"""
兼职信息发送推送
"""


class meituan_jober:

    def __init__(self):
        self.rdb = RedisDBHelper(8)
        self.mdb = MysqlPool()

        self.jobs_group = [
            "1170625269",
            "855015506"
        ]

    def get_formatted_time(self, ):
        # 获取当前时间
        now = datetime.now()

        # 使用strftime格式化时间
        formatted_time = now.strftime("%Y年%m月%d日 %H:%M:%S")

        # 打印格式化后的时间
        # print(f"格式化后的时间: {formatted_time}")
        return formatted_time

    def get_current_time(self, ):
        # 获取当前时间
        now = datetime.now()

        # 分别获取年、月、日、时、分、秒
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        second = now.second

        # 打印或返回这些值
        # print(f"当前时间: {year}年{month}月{day}日 {hour}:{minute}:{second}")
        return year, month, day, hour, minute, second

    def total_count(self, data):
        """
        统计字典中，某字段出现的次数
        :return:
        """
        # 提取所有 data_channel 值
        channels = [d['data_channel'] for d in data]

        # 使用 Counter 统计每个 data_channel 出现的次数
        channel_counts = Counter(channels)

        # 将结果转换为列表并按出现次数降序排序
        sorted_channels = sorted(channel_counts.items(), key=lambda x: x[1], reverse=True)

        # 输出结果
        # print(sorted_channels)
        return sorted_channels

    def get_display_width(self, s):
        """计算字符串的显示宽度，考虑中文字符占两个位置"""
        width = 0
        for c in s:
            if unicodedata.east_asian_width(c) in ('F', 'W'):
                width += 2
            else:
                width += 1
        return width

    def format_fixed_length_string(self, total_length, start_data, end_data):
        # 计算数据部分的显示宽度
        start_width = self.get_display_width(start_data)
        end_width = self.get_display_width(end_data)
        data_width = start_width + end_width

        # 检查总长度是否足够容纳数据
        if total_length < data_width:
            raise ValueError("Total length is too short to contain the given data.")

        # 计算中间空格的数量
        space_length = total_length - data_width

        # 构建最终的字符串
        formatted_string = start_data + ' ' * space_length + end_data

        return formatted_string

    def send_group_message(self, group_id, text):
        """
        发送群信息
        :param group_id:
        :param text:
        :return:
        """
        # 定义目标URL
        url = "http://192.168.31.26:53001/send_group_msg"

        # 构建消息体
        payload = {
            "group_id": group_id,
            "message": [
                {
                    "type": "text",
                    "data": {
                        "text": text
                    }
                }
            ]
        }

        # 发送POST请求
        response = requests.post(url, json=payload)

        # 检查响应状态码
        if response.status_code == 200:
            print(f"群：{group_id} 请求成功")
            # 解析并打印响应内容
            return response.json()
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None

    def send_group_sum_message(self, group_id, texts):
        """
        发送合并群信息
        :param group_id:
        :param text:
        :return:
        """
        # 定义目标URL
        url = "http://192.168.31.26:53001/send_group_forward_msg"
        msgs = [
            {
                "type": "node",
                "data": {
                    "user_id": "855015506",
                    "nickname": "神勇小菊花",
                    "content": {
                        "type": "text",
                        "data": {
                            "text": t
                        }
                    }
                }
            }

            for t in texts
        ]
        # 构建消息体
        payload = {
            "group_id": group_id,
            "messages": msgs
        }

        # 发送POST请求
        response = requests.post(url, json=payload)

        # 检查响应状态码
        if response.status_code == 200:
            print(f"群：{group_id} 请求成功")
            # 解析并打印响应内容
            return response.json()
        else:
            print(f"请求失败，状态码：{response.status_code}")
            return None

    def send_jobs_msg(self, ):
        """
        发送任务信息
        :return:
        """
        # 读取redis上的任务
        jobs = self.rdb.lrange("mt_store_list", 0, -1) or []

        res = [
            f"-*- 兼职监控 -*-",
            f"发现待滑药店列表！",
            f"药店数量：{len(jobs)} ",
            f"检测时间：{self.get_formatted_time()} ",
            f"-*- 兼职监控 -*-",
        ]
        msg_str = "\n".join(res)

        return jobs, msg_str

    def send_finish_msg(self, ):
        """
        发送任务完成榜
        :return:
        """
        date_str = list(self.get_current_time())
        tmp_date = f"{date_str[0]}-{date_str[1]}-{date_str[2]}"
        sql = f"""
        select data_channel,store_name,count(data_channel) from drug_detail 
        where '{tmp_date}' <update_time 
        and spu_tag_id ='111111111111' group by data_channel,store_name;
        """

        # 读取mysql上的任务
        finish_jobs = self.mdb.fetch_all(sql)

        total = self.total_count(finish_jobs)

        res = [
            "-*- 兼职 龙虎榜 -*-",
            "统计榜有延迟性，仅供参考。",
        ]
        for i, f in enumerate(total, start=1):
            t = self.format_fixed_length_string(30, f"{i}.{f[0].replace('zidonghua1.0_', '')}", f"{f[1]} 家")
            res.append(f"   {t};")

        res.append(f"统计时间：{self.get_formatted_time()}")
        res.append("-*- 兼职 龙虎榜 -*-")
        msg_str = "\n".join(res)
        # print(msg_str)
        # 任务为空时，不发信息
        if not len(finish_jobs):
            return None, None

        return finish_jobs, msg_str

    # 统一信息发送
    def all_send(self, wait_msg):
        """
        统一信息发送
        :param wait_msg:
        :return:
        """
        wait_msg = [i for i in wait_msg if i]
        # 发送群信息
        for g in self.jobs_group:
            result = self.send_group_sum_message(g, wait_msg)
            # if result is not None:
            #     print(json.dumps(result, indent=4))

    def is_within_time_range(self, ):
        """
        时间段运行
        :return:
        """
        import datetime
        # 获取当前时间
        now = datetime.datetime.now()

        # 定义时间范围
        start_time = datetime.time(9, 30)
        end_time = datetime.time(23, 30)

        # 判断当前时间是否在指定范围内
        if start_time <= now.time() <= end_time:
            return True
        else:
            return False

    def main_process(self, interval=60):
        """
        主程序，执行各项流程
        :return:
        """
        last_jobs_value = None  # 上次jobs检测值
        last_send_time = None  # 上次发送信息的时间
        while True:
            if not self.is_within_time_range():
                print("当前时间不在9点半到23点半之间，退出循环")
                break

            wait_msg = []  # 待发送信息

            # 发送任务池信息
            jobs, j_msg = self.send_jobs_msg()
            # 发送任务榜信息
            finish_jobs, f_msg = self.send_finish_msg()

            wait_msg.append(j_msg)
            wait_msg.append(f_msg)

            if last_send_time is None or len(jobs) != len(last_jobs_value):
                if last_send_time is None or (datetime.now() - last_send_time) > timedelta(minutes=10):
                    self.all_send(wait_msg)
                    last_send_time = datetime.now()  # 更新上次发送信息的时间
                    last_jobs_value = jobs
                else:
                    print("信息发动cd未冷却...")
            else:
                print(f"{datetime.now()} 药店列表没有变化...")

            time.sleep(interval)


if __name__ == '__main__':
    mtj = meituan_jober()
    mtj.main_process()
