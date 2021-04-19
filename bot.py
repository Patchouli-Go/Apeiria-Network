#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot import log
from apeiria_network.log import logger
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

# Custom your logger
#
# from nonebot.log import logger, default_format
# logger.add("error.log",
#            rotation="00:00",
#            diagnose=False,
#            level="ERROR",
#            format=default_format)

# You can pass some keyword args config to init function
nonebot.init()

# nonebot.init(apscheduler_config={
#     "apscheduler.timezone": "Asia/Shanghai"
# })
# nonebot.init(apscheduler_autostart=True)

app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

nonebot.load_builtin_plugins()
nonebot.load_plugin("apeiria_network.plugins.weather")
nonebot.load_plugin("apeiria_network.plugins.notice")
nonebot.load_plugin("apeiria_network.plugins.repeat")
nonebot.load_plugin("apeiria_network.plugins.status")
nonebot.load_plugin("apeiria_network.plugins.switch")
nonebot.load_plugin("apeiria_network.plugins.chat")
nonebot.load_plugin("apeiria_network.plugins.russian_roulette")
# nonebot.load_plugins("apeiria_network/plugins")
nonebot.load_from_toml("pyproject.toml")

logger.info("Apeiria-Network Status OK")

# Modify some config / config depends on loaded configs
#
# config = driver.config
# do something...


if __name__ == "__main__":
    nonebot.logger.warning(
        "Always use `nb run` to start the bot instead of manually running!"
    )
    nonebot.run(app="__mp_main__:app")
