import nonebot

import json

from nonebot import require

from nonebot import get_driver

from pathlib import Path

from .config import Config

from ..weather.data_source import (
    getAreaJson,
    randomPositive,
    weather_info,
    now_time,
    WEATHER_REPLY,
    answer_sexcall_akubi,
)


global_config = get_driver().config
config = Config(**global_config.dict())
master = global_config.superusers
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass


scheduler = require("nonebot_plugin_apscheduler").scheduler


@scheduler.scheduled_job(
    "cron",
    minute="30",
    hour="1-23/3",
    day_of_week="mon,tue,wed,thu,fri,sat,sun",
    misfire_grace_time=60,
)
async def run_every_1_5_hour():
    if 1 < now_time() < 7:
        pass
    else:
        self_id = global_config.self_id
        bot = nonebot.get_bots()[str(self_id)]
        group = {676859742}
        img = (
            Path(".")
            / "apeiria_network"
            / "data"
            / "img"
            / "notice"
            / "drink_water.jpg"
        )
        img = img.resolve()
        msg = f"[CQ:image,file=file:///{img}]"
        for group_id in group:
            await bot.call_api("send_group_msg", group_id=group_id, message=msg)


@scheduler.scheduled_job(
    "cron",
    minute="0",
    hour="0-23/3",
    day_of_week="mon,tue,wed,thu,fri,sat,sun",
    misfire_grace_time=60,
)
async def run_every_1_5_hour():
    if 1 < now_time() < 7:
        pass
    else:
        self_id = global_config.self_id
        bot = nonebot.get_bots()[str(self_id)]
        group = {676859742}
        img = (
            Path(".")
            / "apeiria_network"
            / "data"
            / "img"
            / "notice"
            / "drink_water.jpg"
        )
        img = img.resolve()
        msg = f"[CQ:image,file=file:///{img}]"
        for group_id in group:
            await bot.call_api(api="send_group_msg", group_id=group_id, message=msg)


@scheduler.scheduled_job(
    "cron", hour="8", day_of_week="mon,tue,wed,thu,fri,sat,sun", misfire_grace_time=60
)
async def daily_weather():
    self_id = global_config.self_id
    bot = nonebot.get_bots()[str(self_id)]
    users = {"564226778"}
    area_reader = getAreaJson()
    for user_id in users:
        cityname = area_reader[user_id]
        weatherinfo = weather_info(cityname, 0)
        dc = json.loads(weatherinfo.text)

        member_info = await bot.call_api("get_stranger_info", user_id=user_id)
        card = ""
        args = answer_sexcall_akubi(
            member_info=member_info, user=user_id, master=master, card=card
        )
        answer = args[0]
        sexcall = args[1]
        akubi = args[2]

        msg = dc["showapi_res_body"]
        now = msg["now"]
        f1 = msg["f1"]
        msg = WEATHER_REPLY.format(
            positive=randomPositive(),
            answer=answer,
            sexcall=sexcall,
            area=now["aqiDetail"]["area"],
            akubi=akubi,
            realtime=now["temperature_time"],
            realweather=now["weather"],
            realtempt=now["temperature"],
            realwinddirect=now["wind_direction"],
            realwindpower=now["wind_power"],
            dayweather=f1["day_weather"],
            daytempt=f1["day_air_temperature"],
            daywinddirect=f1["day_wind_direction"],
            daywindpower=f1["day_wind_power"],
            nightweather=f1["night_weather"],
            nighttempt=f1["night_air_temperature"],
            nightwinddirect=f1["night_wind_direction"],
            nightwindpower=f1["night_wind_power"],
            clothrec=f1["index"]["clothes"]["desc"],
        )
        await bot.call_api(api="send_private_msg", user_id=user_id, message=msg)


# 测试用定时任务
# @scheduler.scheduled_job('cron', minute='*/1', day_of_week="mon,tue,wed,thu,fri,sat,sun", misfire_grace_time=60)
# async def run_every_1_5_hour():
#     self_id=global_config.self_id
#     bot = nonebot.get_bots()[str(self_id)]
#     group = {721087756, 676859742}#676859742
#     img = Path('.') / 'apeiria_network' / 'data' / 'img' / 'notice' / 'drink_water.jpg'
#     img = img.resolve()
#     msg = f'[CQ:image,file=file:///{img}]'
#     for group_id in group:
#         await bot.call_api(api='send_group_msg', group_id=group_id, message=msg)
