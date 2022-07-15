#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter


# 自定义日志对象
from nonebot.log import logger, default_format
logger.add("error.log",
           rotation="00:00",
           diagnose=False,
           level="ERROR",
           format=default_format)

"""
运行主程
"""
nonebot.init()
app = nonebot.get_asgi()
driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)
# 读取driver配置项
config = driver.config
# bot启动时执行的init
# driver.on_startup(init)
# bot关闭时执行的disconnect
# driver.on_shutdown(disconnect)

# 插件加载
nonebot.load_builtin_plugins("echo")
# pyproject.toml读取各项配置
nonebot.load_from_toml("pyproject.toml")


if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
