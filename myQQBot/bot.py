#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter as ONEBOT_V11Adapter

nonebot.init()

# 加载插件目录
nonebot.load_plugins("src/plugins")
nonebot.load_plugins("src/plugins/zdhf")
nonebot.load_plugins("src/plugins/timework/__init__.py")
nonebot.load_plugin("nonebot_plugin_songpicker2")
# nonebot.load_plugin("nonebot_plugin_boardgame")
# nonebot.load_plugin("nonebot_plugin_cchess")
# nonebot.load_plugin("nonebot_plugin_setu4")
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(ONEBOT_V11Adapter)

nonebot.load_builtin_plugins()  # 加载 nonebot 内置插件

if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
