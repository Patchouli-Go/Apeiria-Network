# import nonebot
import json

from apeiria_network.plugins.weather.data_source import randomNegative
from pathlib import Path
from nonebot import on_command, get_driver
from nonebot.adapters.cqhttp.message import Message
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event

from random import choice, randint

from .config import Config
import fcntl

import redis

global_config = get_driver().config
config = Config(**global_config.dict())

r = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)
"""
俄罗斯转盘
	判断会话状态是否为active
		是，则读取子弹数量，开枪次数，命中数。
		否，则初始化数据，初始化 子弹数量，开枪次数，命中数。
开始会话
	每个人触发几率为子弹数/6-开枪次数
	触发命中后，子弹数量-1，开枪次数+1，命中+1，返回命中讯息
	触发miss后，子弹数量不变，开枪次数+1，命中不变，返回miss讯息
	当命中数=子弹数时，总会话终止，设置会话状态false
"""


shoot = on_command("开枪", rule=None, priority=2)


@shoot.handle()
async def _(bot: Bot, event: Event, state: T_State):
    message_type = str(event.dict()["message_type"])
    # 来源判断
    if message_type == "group":
        id = str(event.dict()["group_id"])
        # ru = Path(".") / "apeiria_network" / "config" / "ru" / "group" / "ru.json"
    elif message_type == "private":
        id = event.get_user_id()
        # ru = Path(".") / "apeiria_network" / "config" / "ru" / "private" / "ru.json"
    # strmsg = [0, 0, 0, 0]
    # ru_status = strmsg[0]
    # bullets_num = strmsg[1]
    # shoot_times = strmsg[2]
    # hit_times = strmsg[3]

    # 为None或没有则初始化
    try:
        strmsg = r.get("ru"+id).split(',')
    except:
        r.set("ru"+id, ','.join(['0','0','0','0']))
        strmsg = r.get("ru"+id).split(',')

    args = str(event.get_message()).strip()
    if args:
        # 子弹数非法结束
        if not (int(args) >= 1 and int(args) <= 6):
            await shoot.finish(randomNegative() + "请输入1到6以内的数字重试")
        # 判断会话状态是否为active
        if strmsg[0] == '0':
            # 否，则初始化数据，初始化 子弹数量，开枪次数，命中数。
            strmsg[0] = '1'
            strmsg[1] = args
            strmsg[2] = '0'
            strmsg[3] = '0'
            # print(strmsg)
            # ru_json_file_w = open(ru, mode="w", encoding="utf-8")
            # json.dump(strmsg, ru_json_file_w, ensure_ascii=False)
            r.set("ru"+id, ','.join(strmsg))
            r.set("death" + id, "")
            r.set("alive" + id, "")
            magazine = []
            for i in range(0, 6 - int(strmsg[1])):
                magazine.append("0")
            for i in range(0, int(strmsg[1])):
                magazine.insert(randint(0, len(magazine)), "1")
            r.set("magazine" + id, ",".join(magazine))
            bul = choice(
                [
                    "子弹装好了",
                    "子弹填充完毕~",
                    "LMG MOUNTED AND LOADED",
                    "五十已到",
                ]
            )
            await shoot.finish(bul)
        else:
            # 是，则读取子弹数量。
            await shoot.finish("之前的转盘活动并没有迎来结局，请完成上一场活动之后再开始新的活动")
    else:
        # 判断会话状态是否为active
        if strmsg[0] == '1':
            state["bullets_num"] = strmsg[1]
            # state["ru"] = ru
            state["id"] = id
        elif strmsg[0] == '0':
            # state["ru"] = ru
            state["id"] = id


@shoot.got("bullets_num", prompt="欢迎参与紧张刺激的俄罗斯轮盘活动，请输入要填入的子弹数目(最多6颗)")
async def _(bot: Bot, event: Event, state: T_State):
    message_type = str(event.dict()["message_type"])
    user_id = event.get_user_id()
    try:
        bullets_num = int(state["bullets_num"])
    except:
        await shoot.finish(randomNegative() + "请输入1到6以内的数字重试")
    # ru = state["ru"]
    id = state["id"]
    strmsg = r.get("ru"+id).split(',')
    # 子弹数非法结束
    if not (bullets_num >= 1 and bullets_num <= 6):
        await shoot.finish(randomNegative() + "请输入1到6以内的数字重试")
    if strmsg[0] == '0':
        # 初始化数据，初始化 子弹数量，开枪次数，命中数
        strmsg[0] = '1'
        strmsg[1] = str(bullets_num)
        strmsg[2] = '0'
        strmsg[3] = '0'
        r.set("ru"+id, ','.join(strmsg))
        r.set("death" + id, "")
        r.set("alive" + id, "")
        magazine = []
        for i in range(0, 6 - int(strmsg[1])):
            magazine.append("0")
        for i in range(0, int(strmsg[1])):
            magazine.insert(randint(0, len(magazine)), "1")
        r.set("magazine" + id, ",".join(magazine))
        bul = choice(
            [
                "子弹装好了",
                "子弹填充完毕~",
                "LMG MOUNTED AND LOADED",
                "五十已到",
            ]
        )
        await shoot.finish(bul)
    if r.get("death" + id) == None:
        r.set("death" + id, "")
    if r.get("alive" + id) == None:
        r.set("alive" + id, "")
    # print(r.get("magazine"+id))
    magazine = r.get("magazine" + id).split(",")
    # print(magazine)
    
    # if randint(1, (6 - strmsg[id][2])) <= strmsg[id][1]:
    if magazine[0] == "1":
        # 随机1到剩余开枪次数 小于等于子弹数量时命中
        # 命中 开枪次数+1 击中+1
        magazine.pop(0)
        r.set("magazine" + id, ",".join(magazine))
        strmsg[2] = str((int(strmsg[2])+1))
        strmsg[3] = str((int(strmsg[3])+1))
        r.set("ru"+id, ','.join(strmsg))
        msg = [
            ["很不幸，你死了"],
            ["砰！枪响人亡"],
            ["砰！枪响人亡", "你死了"],
            ["开完这枪，我就回家和老婆结婚\n——你如是宣言到", "汝之妻，吾养之\nYou Died...."],
            ["你是一个有故事的人，但是子弹并不想知道这些\n它只看见了白花花的脑浆", "你死了"],
            ["啦哒哒哒哒！啦哒哒哒哒！", "You Died...."],
            ["BOOOOOM HEADSHOT!!", "You Died...."],
            ["哒哒哒哒哒！", "啊，你死了"],
        ]
        # r.sadd("death"+id, event.get_session_id()+",")
        if message_type == "group":
            group_id = str(event.dict()["group_id"])
            member_info = await bot.call_api(
                "get_group_member_info", group_id=group_id, user_id=user_id
            )
            card = member_info["card"]
        elif message_type == "private":
            member_info = await bot.call_api("get_stranger_info", user_id=user_id)
            card = ""
        nickname = member_info["nickname"]
        if card == "" or card == None:
            call = nickname
        else:
            call = card
        r.set("death" + id, r.get("death" + id) + call + ",")
        for a in msg[randint(0, len(msg) - 1)]:
            await bot.send(event, a)
    else:
        # miss 开枪次数+1
        magazine.pop(0)
        r.set("magazine" + id, ",".join(magazine))
        strmsg[2] = str((int(strmsg[2])+1))
        r.set("ru"+id, ','.join(strmsg))
        msg = [
            ["哦？你侥幸活了下来呢~"],
            ["砰！\n随着一声清脆的枪响，你...", "不好意思，念错了"],
            ["你对此胸有成竹，你曾经在精神病院向一个老汉学习过用手指夹住射出子弹的功夫，在子弹射出的一瞬间，你把他塞了回去"],
            ["你向众神祈祷，众神仿佛听见了你的呼唤", "你自信的扣下了扳机，当然，枪没有响"],
            ["治疗感染，一次...什么？你没有感染？出去！！"],
            ["你颤抖的手写完了遗书上的最后一个字", "虽然很抱歉，但是这张纸可以留到以后再用了"],
            # ["冰冷的子弹击中了你的牛子\n你活了下来","但是你的牛子没了，你试问\n这一切都值得吗"],
            # ["你非常的确信，枪膛里下一发是有子弹的","但是这颗子弹火药貌似受潮了~\n恭喜你捡回了一条小命"],
        ]
        # r.sadd("alive"+id, event.get_session_id()+",")
        # r.set("alive"+id, r.get("alive"+id)+event.get_session_id()+",")
        if message_type == "group":
            group_id = str(event.dict()["group_id"])
            member_info = await bot.call_api(
                "get_group_member_info", group_id=group_id, user_id=user_id
            )
            card = member_info["card"]
        elif message_type == "private":
            member_info = await bot.call_api("get_stranger_info", user_id=user_id)
            card = ""
        nickname = member_info["nickname"]
        if card == "" or card == None:
            call = nickname
        else:
            call = card
        r.set("alive" + id, r.get("alive" + id) + call + ",")
        for a in msg[randint(0, len(msg) - 1)]:
            await bot.send(event, a)
    if int(strmsg[3]) >= int(strmsg[1]):
        # 命中次数 == 子弹次数 结束会话
        strmsg[0] = strmsg[1] = strmsg[2] = strmsg[3] = '0'
        r.set("ru"+id, ','.join(strmsg))
        death = r.get("death" + id).strip(",").split(",")
        alive = r.get("alive" + id).strip(",").split(",")
        count = {}
        for de in death:
            count.update({de: [0, death.count(de)]})
        if alive != [""]:
            # print(alive)
            for al in alive:
                try:
                    a = count[al][1]
                except:
                    a = 0
                count.update({al: [alive.count(al), a]})
        # print(count)
        r.set("death" + id, "")
        r.set("alive" + id, "")
        r.set("magzine" + id, "")
        msg = ""
        i = 0
        for c in count:
            i += 1
            msg += c + "：胜利" + str(count[c][0]) + " 死亡" + str(count[c][1])
            if i != len(count):
                msg += "\n"
        await bot.send(event, "感谢各位的参与，让我们看一下游戏结算：")
        await shoot.finish(msg)
    await bot.send(
        event,
        "欢迎下一位。已经开了"
        + strmsg[2]
        + "枪，还剩"
        + str(int(strmsg[1]) - int(strmsg[3]))
        + "发子弹。",
    )


clearshoot = on_command("清空弹仓", rule=None, priority=2)


@clearshoot.handle()
async def _(bot: Bot, event: Event, state: T_State):
    message_type = str(event.dict()["message_type"])
    if message_type == "group":
        id = str(event.dict()["group_id"])
        # ru = Path(".") / "apeiria_network" / "config" / "ru" / "group" / "ru.json"
    elif message_type == "private":
        id = event.get_user_id()
    try:
        strmsg = r.get("ru"+id).split(',')
    except:
        r.set("ru"+id, ','.join(['0','0','0','0']))
        strmsg = r.get("ru"+id).split(',')
    strmsg[0] = strmsg[1] = strmsg[2] = strmsg[3] = '0'
    r.set("ru"+id, ','.join(strmsg))
    r.set("death" + id, "")
    r.set("alive" + id, "")
    r.set("magzine" + id, "")
    await clearshoot.finish("已清空弹仓")
