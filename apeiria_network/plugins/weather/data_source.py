import json

import requests

from datetime import datetime

from pathlib import Path

from random import choice

from nonebot import get_driver

from apeiria_network.log import logger

global_config = get_driver().config
debug = global_config.debug


# 天气回复信息模板
WEATHER_REPLY = """{positive}{answer}{sexcall}，{area}今日气象数据如下：{akubi}
实时气象： {realtime}，{realweather}，{realtempt}°C，{realwinddirect}，风力{realwindpower}
白天：{dayweather}，{daytempt}°C，{daywinddirect}，风力{daywindpower}
夜间：{nightweather}，{nighttempt}°C，{nightwinddirect}，风力{nightwindpower}
{clothrec}"""

AREA_PATH = Path(".") / "apeiria_network" / "data" / "weather" / "area.json"


# 时间判断函数


def getAreaJson():
    try:
        with open(AREA_PATH, mode="r", encoding="utf-8") as f:
            area_reader = json.load(f)
            return area_reader
    except:
        area_reader = {}
        return area_reader

def now_time():
    now_ = datetime.now()
    hour = now_.hour
    minute = now_.minute
    now = hour + minute / 60
    return now


def randomPositive():
    return choice(
        [
            "Positive，",
            "Positive！",
        ]
    )


def randomNegative():
    return choice(
        [
            "Negative，",
            "Negative！",
            "Negative...",
        ]
    )


# 绑定城市函数


def answer_sexcall_akubi(member_info, user, master, card):
    sex = member_info["sex"]
    age = member_info["age"]
    if member_info["sex"] == "male":
        if age <= 24:
            sexcall = "君"
        else:
            sexcall = "桑"
    elif sex == "female":
        if age <= 24:
            sexcall = "酱"
        else:
            sexcall = "桑"
    else:
        sexcall = "桑"

    nickname = member_info["nickname"]
    M = False
    if user in master:
        M = True
    if M is True:
        sexcall = ""
        call = "Owner"
    else:
        if card == "" or card == None:
            call = nickname
        else:
            call = card

    akubi = ""
    answer = ""
    if 5.5 <= now_time() < 8:
        answer = choice(["早上好，真早呢，", "(哈欠)早..."]) + call
    elif 8 <= now_time() < 12:
        answer = (
            choice(
                [
                    "早上好，",
                    "おはいよ，",
                    "早上好！",
                    "おはいよ！",
                    "Good Morning！",
                ]
            )
            + call
        )
    elif 12 <= now_time() < 14:
        answer = "中午好，" + call
    elif 14 <= now_time() < 18:
        answer = "下午好，" + call
    elif 18 <= now_time() < 24:
        answer = choice(["空帮哇，", "こんばんわ，"]) + call
    elif 0 <= now_time() < 5.5:
        answer = "呜呜。。" + call + "，现在是深夜诶。。。"
        akubi = "唔啊啊..."

    args = (answer, sexcall, akubi)
    return args


def _weather_bind(user, cityname):
    data = {user: cityname}
    area_reader = getAreaJson()
    with open(AREA_PATH, mode="w", encoding="utf-8") as area_json_file_w:
        if user in area_reader:
            area_reader[user] = cityname
        else:
            area_reader.update(data)
        json.dump(area_reader, area_json_file_w, ensure_ascii=False)


# @drivers.Driver.on_bot_connect
# async def connect(bot) -> None:


# 查询天气函数
def weather_info(area_name, pre):
    # 以下需要修改
    global html
    appcode = global_config.weather_key
    req_data = {"area": area_name, "needIndex": "1", "needMoreDay": pre}
    # 修改结束
    url = "https://weather01.market.alicloudapi.com/area-to-weather"
    headers = {"Authorization": "APPCODE " + appcode}
    try:
        html = requests.get(url, headers=headers, data=req_data)
    except:
        print("URL错误")
        exit()
    if debug is True:
        print("---------response status is:-------------")
        print(html.status_code)
        print("---------response headers are:-------------")
        print(html.headers)
        msg = html.headers.get("X-Ca-Error-Message")
        status = html.status_code

        if status == 200:
            print("status为200，请求成功，计费1次。（status非200时都不计费）")
        else:
            if status == 400 and msg == "Invalid AppCode":
                print(
                    "AppCode不正确，请到用户后台获取正确的AppCode： https://market.console.aliyun.com/imageconsole/index.htm"
                )
            elif status == 400 and msg == "Invalid Path or Method":
                print("url地址或请求的'GET'|'POST'方式不对")
            elif status == 403 and msg == "Unauthorized":
                print("服务未被授权,请检查是否购买")
            elif status == 403 and msg == "Quota Exhausted":
                print("套餐资源包次数已用完")
            elif status == 500:
                print("API网关错误")
            else:
                print("参数名错误或其他错误")
                print(status)
                print(msg)

        print("---------response body is:-------------")
        print(html.text)
    else:
        logger.info("response status is:" + str(html.status_code))
    return html
