import json
import time

# from apeiria_network.log import logger

# from random import choice

# from pathlib import Path

from .data_source import (
    getAreaJson,
    randomNegative,
    randomPositive,
    weather_info,
    _weather_bind,
    WEATHER_REPLY,
    answer_sexcall_akubi,
)

from .config import Config

from nonebot import on_command, get_driver
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event


global_config = get_driver().config
config = Config(**global_config.dict())
master = global_config.superusers
# print(master)
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"
#
# @export.xxx
# def some_function():
#     pass


# 天气功能
weather = on_command("天气", rule=None, priority=2)


@weather.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    user_id = event.get_user_id()
    area_reader = getAreaJson()
    if args:
        state["city"] = args  # 如果用户发送了参数则直接赋值
    elif user_id in area_reader:
        state["city"] = area_reader[user_id]


@weather.got("city", prompt="你想查询哪个城市的天气呢？\n第一次查询会自动绑定你的城市")
async def handle_city(bot: Bot, event: Event, state: T_State):
    startTime = time.perf_counter()
    cityname = state["city"]
    weatherinfo = weather_info(cityname, 0)
    responsecode = weatherinfo.status_code
    user_id = event.get_user_id()
    area_reader = getAreaJson()
    # 判断查询
    if cityname[0:2] == "天气":
        cityname = str(cityname[2 : len(cityname)]).strip()
        # 第一次查询绑定
        if user_id not in area_reader:
            if responsecode == 555:
                await weather.finish(randomNegative() + "查询失败，地名输入错误")
            elif responsecode == 403:
                await weather.finish(randomNegative() + "API访问次数用完了，请续费API")
            _weather_bind(user=user_id, cityname=cityname)
            msg = "绑定成功，如果要更换绑定城市\n可使用[天气绑定 城市名]"
    # 第一次查询绑定
    elif user_id not in area_reader:
        if responsecode == 555:
            await weather.finish(randomNegative() + "查询失败，地名输入错误")
        elif responsecode == 403:
            await weather.finish(randomNegative() + "API访问次数用完了，请续费API")
        _weather_bind(user=user_id, cityname=cityname)
        msg = "绑定成功，如果要更换绑定城市\n可使用[天气绑定 城市名]"
        await bot.send(event=event, message=msg)

    message_type = str(event.dict()["message_type"])
    dc = json.loads(weatherinfo.text)

    if responsecode == 555:
        await weather.finish(randomNegative() + "地名输入错误")
    elif responsecode == 403:
        await weather.finish(randomNegative() + "API访问次数用完了，请续费API")

    if message_type == "group":
        group_id = str(event.dict()["group_id"])
        member_info = await bot.call_api(
            "get_group_member_info", group_id=group_id, user_id=user_id
        )
        card = member_info["card"]
    elif message_type == "private":
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

    city_weather = WEATHER_REPLY.format(
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
    endTime = time.perf_counter()
    times = round(endTime - startTime, 3)
    city_weather += "\n------------------------\n"
    city_weather += "Complete time:" + str(times) + "s"
    await weather.finish(city_weather)


# @weather.got("city", prompt='你想查询哪个城市的天气呢？\n可以输入"天气绑定 城市名"来绑定你的城市')
# async def handle_city(bot: Bot, event: Event, state: T_State):
#     cityname = state["city"]
#     user_id = event.get_user_id()
#     if cityname[0:4] == "天气绑定":
#         # print("cityname[0:4]:"+cityname[0:4])
#         cityname = str(cityname[4 : len(cityname)]).strip()
#         # print(cityname)
#         weatherinfo = weather_info(cityname, 0)
#         responsecode = weatherinfo.status_code
#         if responsecode == 555:
#             await weather.finish(randomNegative() + "绑定失败，地名输入错误")
#         elif responsecode == 403:
#             await weather.finish(randomNegative() + "API访问次数用完了，请续费API")

#         _weather_bind(user=user_id, cityname=cityname)
#         await weather.finish("绑定成功")
#     elif cityname[0:2] == "天气":
#         cityname = str(cityname[2 : len(cityname)]).strip()

#     message_type = str(event.dict()["message_type"])
#     weatherinfo = weather_info(cityname, 0)
#     dc = json.loads(weatherinfo.text)
#     responsecode = weatherinfo.status_code

#     if responsecode == 555:
#         await weather.finish(randomNegative() + "地名输入错误")
#     elif responsecode == 403:
#         await weather.finish(randomNegative() + "API访问次数用完了，请续费API")

#     if message_type == "group":
#         group_id = str(event.dict()["group_id"])
#         member_info = await bot.call_api(
#             "get_group_member_info", group_id=group_id, user_id=user_id
#         )
#         card = member_info["card"]
#     elif message_type == "private":
#         member_info = await bot.call_api("get_stranger_info", user_id=user_id)
#         card = ""

#     args = answer_sexcall_akubi(
#         member_info=member_info, user=user_id, master=master, card=card
#     )
#     answer = args[0]
#     sexcall = args[1]
#     akubi = args[2]

#     msg = dc["showapi_res_body"]
#     now = msg["now"]
#     f1 = msg["f1"]

#     city_weather = WEATHER_REPLY.format(
#         positive=randomPositive(),
#         answer=answer,
#         sexcall=sexcall,
#         area=now["aqiDetail"]["area"],
#         akubi=akubi,
#         realtime=now["temperature_time"],
#         realweather=now["weather"],
#         realtempt=now["temperature"],
#         realwinddirect=now["wind_direction"],
#         realwindpower=now["wind_power"],
#         dayweather=f1["day_weather"],
#         daytempt=f1["day_air_temperature"],
#         daywinddirect=f1["day_wind_direction"],
#         daywindpower=f1["day_wind_power"],
#         nightweather=f1["night_weather"],
#         nighttempt=f1["night_air_temperature"],
#         nightwinddirect=f1["night_wind_direction"],
#         nightwindpower=f1["night_wind_power"],
#         clothrec=f1["index"]["clothes"]["desc"],
#     )
#     await weather.finish(city_weather)


# async def get_weather(city: str):
#     return f"{city}"


# 天气绑定功能
weather_bind = on_command("天气绑定", rule=None, priority=2)


@weather_bind.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if args:
        state["city"] = args  # 如果用户发送了参数则直接赋值


@weather_bind.got("city", prompt="输入你想要绑定的城市")
async def handle_city(bot: Bot, event: Event, state: T_State):
    user = event.get_user_id()
    cityname = state["city"]
    weatherinfo = weather_info(cityname, 0)
    responsecode = weatherinfo.status_code
    if responsecode == 555:
        await weather_bind.finish(randomNegative() + "绑定失败，地名输入错误")
    elif responsecode == 403:
        await weather_bind.finish(randomNegative() + "API访问次数用完了，请续费API")

    _weather_bind(user=user, cityname=cityname)
    await weather_bind.finish("绑定成功")


weather_pre_report = on_command("天气预报", rule=None, priority=2)


@weather_pre_report.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    user_id = event.get_user_id()
    area_reader = getAreaJson()
    if args:
        state["city"] = args  # 如果用户发送了参数则直接赋值
    elif user_id in area_reader:
        state["city"] = area_reader[user_id]


@weather_pre_report.got("city", prompt="你想查询哪个城市的天气预报呢？\n第一次查询会自动绑定你的城市")
async def handle_city(bot: Bot, event: Event, state: T_State):
    startTime = time.perf_counter()
    cityname = state["city"]
    weatherinfo = weather_info(cityname, 1)
    responsecode = weatherinfo.status_code
    user_id = event.get_user_id()
    area_reader = getAreaJson()
    # 判断查询
    if cityname[0:2] == "天气预报":
        cityname = str(cityname[2 : len(cityname)]).strip()
        # 第一次查询绑定
        if user_id not in area_reader:
            if responsecode == 555:
                await weather_pre_report.finish(randomNegative() + "查询失败，地名输入错误")
            elif responsecode == 403:
                await weather_pre_report.finish(randomNegative() + "API访问次数用完了，请续费API")
            _weather_bind(user=user_id, cityname=cityname)
            msg = "绑定成功，如果要更换绑定城市\n可使用[天气绑定 城市名]"
    # 第一次查询绑定
    elif user_id not in area_reader:
        if responsecode == 555:
            await weather_pre_report.finish(randomNegative() + "查询失败，地名输入错误")
        elif responsecode == 403:
            await weather_pre_report.finish(randomNegative() + "API访问次数用完了，请续费API")
        _weather_bind(user=user_id, cityname=cityname)
        msg = "绑定成功，如果要更换绑定城市\n可使用[天气绑定 城市名]"
        await bot.send(event=event, message=msg)

    message_type = str(event.dict()["message_type"])
    dc = json.loads(weatherinfo.text)

    if responsecode == 555:
        await weather_pre_report.finish(randomNegative() + "地名输入错误")
    elif responsecode == 403:
        await weather_pre_report.finish(randomNegative() + "API访问次数用完了，请续费API")

    if message_type == "group":
        group_id = str(event.dict()["group_id"])
        member_info = await bot.call_api(
            "get_group_member_info", group_id=group_id, user_id=user_id
        )
        card = member_info["card"]
    elif message_type == "private":
        member_info = await bot.call_api("get_stranger_info", user_id=user_id)
        card = ""

    args = answer_sexcall_akubi(
        member_info=member_info, user=user_id, master=master, card=card
    )
    answer = args[0]
    sexcall = args[1]
    akubi = args[2]
    msg = dc["showapi_res_body"]
    positive = randomPositive()

    # 获取完整天气信息测试
    # FULL_WEATHER_PATH = Path(".") / "weather_full_info.json"

    # with open(FULL_WEATHER_PATH, mode="w", encoding="utf-8") as area_json_file_w:
    #     json.dump(msg, area_json_file_w, ensure_ascii=False)

    msg0 = positive + answer + sexcall + "， 以下为" + cityname + "七日天气预报" + akubi + "\n"
    # msg0 += ""
    for i in range(1, 8):
        curwea = msg["f" + str(i)]
        dayweather = curwea["day_weather"]
        daytempt = curwea["day_air_temperature"]
        nightweather = curwea["night_weather"]
        nighttempt = curwea["night_air_temperature"]
        msg0 += (
            "Day"
            + str(i)
            + " 白天："
            + dayweather
            + "，"
            + daytempt
            + "°C   夜间："
            + nightweather
            + "，"
            + nighttempt
            + "°C\n"
        )
    endTime = time.perf_counter()
    times = round(endTime - startTime, 3)
    msg0 += "------------------------\n"
    msg0 += "Complete time:" + str(times) + "s"
    await weather_pre_report.finish(msg0)


# 测试功能
test = on_command("WeatherTest", rule=None, priority=3)


@test.handle()
async def handle_receive(bot: Bot, event: Event, state: T_State):
    # print(event.get_session_id())
    # group = {721087756}#676859742
    # img = Path('.') / 'apeiria_network' / 'data' / 'img' / 'notice' / 'drink_water.png'
    # # img = os.path.abspath(img)
    # msg = Message(f'[CQ:image,file=file:///{os.path.abspath(img)}]')
    # for group_id in group:
    #     await bot.call_api('send_group_msg', group_id=group_id, message=msg)
    # await test.send(msg)

    await test.finish("testComplete")
