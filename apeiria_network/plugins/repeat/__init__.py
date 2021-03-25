# import nonebot
import json

from pathlib import Path

from nonebot import get_driver

import numpy as np

# from nonebot import on_command, drivers, require

# from nonebot.rule import to_me

from nonebot.plugin import on_message

from nonebot.typing import T_State

from nonebot.adapters.cqhttp import Bot, Event

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass
repeat_after_me = on_message(priority=10)


@repeat_after_me.handle()
async def _(bot: Bot, event: Event, state: T_State):
    # 开关检测，开则复述
    message = event.get_message()
    message_type = str(event.dict()["message_type"])
    # 来源判断
    if message_type == "group":
        id = str(event.dict()["group_id"])
        # message_type = "on_group"
        switch = (
            Path(".")
            / "apeiria_network"
            / "config"
            / "repeat"
            / "group"
            / "switch.json"
        )
        re = Path(".") / "apeiria_network" / "config" / "repeat" / "group" / "re.json"
    elif message_type == "private":
        id = event.get_user_id()
        # message_type = "on_user"
        switch = (
            Path(".")
            / "apeiria_network"
            / "config"
            / "repeat"
            / "private"
            / "switch.json"
        )
        re = Path(".") / "apeiria_network" / "config" / "repeat" / "private" / "re.json"
    try:
        with open(switch, mode="r", encoding="utf-8") as switch_json:
            switch_reader = json.load(switch_json)
    except:
        switch_reader = {}
    if id in switch_reader:
        if switch_reader[id] == "on":
            await repeat_after_me.finish(message)

    # 检测相同信息是否发送三次，若是则复述一次，然后清空数据
    i = 0
    # strmsg = {id: ['', '', '', i, message_type]}
    strmsg = {id: ["", "", "", i]}
    message = str(message)
    try:
        with open(re, mode="r", encoding="utf-8") as re_json:
            strmsg = json.load(re_json)
    except:
        strmsg = {}
    if id not in strmsg:
        with open(re, mode="w", encoding="utf-8") as re_json_file_w:
            # strmsg.update({id: [message, '', '', i, message_type]})
            strmsg.update({id: [message, "", "", i]})
            json.dump(strmsg, re_json_file_w, ensure_ascii=False)
    pos = strmsg[id][3]
    if pos >= 2:
        strmsg[id][pos] = message
        pos -= 3
    else:
        strmsg[id][pos] = message
    pos += 1
    strmsg[id][3] = pos
    if strmsg[id][0] == strmsg[id][1] == strmsg[id][2]:
        strmsg[id][0] = strmsg[id][1] = strmsg[id][2] = ""
        re_json_file_w1 = open(re, mode="w", encoding="utf-8")
        json.dump(strmsg, re_json_file_w1, ensure_ascii=False)
        await repeat_after_me.finish(event.get_message())
    re_json_file_w2 = open(re, mode="w", encoding="utf-8")
    json.dump(strmsg, re_json_file_w2, ensure_ascii=False)
