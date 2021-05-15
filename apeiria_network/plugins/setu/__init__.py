# import nonebot
import datetime
import os
import json
import time
from pathlib import Path
from urllib import request
from random import choice, randint

import nonebot
from nonebot import get_driver, require
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp.message import Message
from nonebot.exception import FinishedException

from apeiria_network.modules.response import request_api_params

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

apikey_LOLI = global_config.apikey_loli
master = global_config.superusers
self_id = global_config.self_id

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

URL = 'https://api.lolicon.app/setu/'

SETU_REPLY = """Title: {title}
Artist: {author}
{setu}
---------------
Complete time:{time}s"""
scheduler = require("nonebot_plugin_apscheduler").scheduler


setu = on_command("setu", aliases={"涩图","色图"}, priority=2)


@setu.handle()
async def _(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    user_id = event.get_user_id()
    message_type = str(event.dict()["message_type"])
    if message_type == "group":
        session_id = str(event.dict()["group_id"])
        if session_id == "875857423":
            raise FinishedException
    elif message_type == "private":
        session_id = user_id
    else:
        await bot.send(event, "不支持的会话！")
        raise FinishedException

    chance = randint(1, 20)
    if 1 <= chance <= 18:
        start = time.perf_counter()
        values = {
            "apikey": apikey_LOLI,
            "r18": "0",
            "num": "1"
        }
        R18 = "false"
        picnum = 1
        direc = Path('/mnt/dm-4/nextcloud/data/patchy/files/pixiv/Normal')

        if msg[0:3] == "r18":
            direc = Path('/mnt/dm-4/nextcloud/data/patchy/files/pixiv/R18')
            R18 = "true"
            values.update({"r18": 1})
            if msg[3:4] == "*":
                # if user_id in master:
                picnum = int(msg[4:5])
                if len(msg) > (msg.index("8") + 3):
                    msg = msg[(msg.index("8") + 3):len(msg)]
                    print(msg)
                    values.update({"keyword": msg})
                # else:
                #     await bot.send(event, '呜，只有主人才能使用这个功能呢')
            elif len(msg) > (msg.index("8") + 1):
                msg = msg[(msg.index("8") + 1):len(msg)]
                print(msg)
                values.update({"keyword": msg})
        elif msg[0:1] == "*":
            # if user_id in master:
            picnum = int(msg[1:2])
            if len(msg) > (3):
                msg = msg[(3):len(msg)]
                print(msg)
                values.update({"keyword": msg})
            # else:
            #     await bot.send(event, '呜，只有主人才能使用这个功能呢')
            #     raise FinishedException
        elif msg:
            values.update({"keyword": msg})
        if picnum > 0:
            await bot.send(event,'别急！正在找图！')
        for x in range(picnum):
            try:
                dc = json.loads(request_api_params(url=URL, params=values))
                if dc["msg"] == 429:
                    await bot.send(event, '今天已经满300张啦！lsp，哼哒！！')
                    raise FinishedException
                print("=========================================")
                print(dc)
                print("=========================================")
                title = dc["data"][0]["title"]
                author = dc["data"][0]["author"]
                setu = dc["data"][0]["url"]  # b64.b64_str_img_url(dc["data"][0]["url"])
            except:
                await bot.send(event, '失败了失败了失败了失...')
                raise FinishedException
            end = time.perf_counter()
            await bot.send(
                event,
                SETU_REPLY.format(
                    title=title,
                    author=author,
                    setu=setu,
                    time=round(end - start, 3)
                )
            )
            try:
                scheduler.add_job(func=getPic, trigger='date', args=[setu, direc, R18, message_type, session_id], next_run_time=datetime.datetime.now(), misfire_grace_time=60)
                pass
            except:
                await bot.send(event, '呜呜，图片获取失败了...')
                raise FinishedException
    elif chance == 19:
        img = choice(
            [
                'SP.jpg', 'SP1.jpg', 'SP2.jpg'
            ]
        )
        img = Path('.') / 'apeiria_network' / 'data' / 'emoji' / f'{img}'
        img = img.resolve()
        await bot.send(event, Message(f'[CQ:image,file=file:///{img}]'))
        raise FinishedException

    elif chance == 20:
        img = choice(
            [
                'GDZ.png', 'SHZY1.jpg', 'SHZY2.jpg', 'SHZY3.jpg', 'SHZY4.jpg', 'SHZY5.jpg', 'SHZY6.jpg'
            ]
        )
        img = Path('.') / 'apeiria_network' / 'data' / 'img' / 'niceIMG' / f'{img}'
        img = img.resolve()
        await bot.send(event, Message(f'[CQ:image,file=file:///{img}]'))
        raise FinishedException

    # else:
    #     await bot.send(event, '该功能已被禁用...')
    #     raise FinishedException


def getPic(url, direc, R18, message_type, session_id):
    # wget.download(url, os.path.abspath(direc), headers=headers)
    opener = request.build_opener()
    opener.addheaders = ([('User-Agent', 'Mozilla/5.0 4240.75 Safari/537.36')])
    request.install_opener(opener)
    request.urlretrieve(url, os.path.abspath(direc) + "/" + os.path.basename(url))
    scheduler.add_job(func=sendPic, trigger='date', args=[url, direc, R18, message_type, session_id], next_run_time=datetime.datetime.now(), misfire_grace_time=60)

async def sendPic(url, direc, R18, message_type, session_id):
    bot = nonebot.get_bots()[str(self_id)]
    if R18 == "false":
        msg = Message(f'[CQ:image,file=file:///{os.path.abspath(direc) + "/" + os.path.basename(url)}]')
        if message_type == "group":
            await bot.call_api(api="send_group_msg", group_id=session_id, message=msg)
        elif message_type == "private":
            await bot.call_api(api="send_private_msg", user_id=session_id, message=msg)