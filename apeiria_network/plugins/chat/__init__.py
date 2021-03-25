# import nonebot
from pathlib import Path
from nonebot import on_command, get_driver
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp.message import MessageSegment as Message

from random import choice

from .config import Config

global_config = get_driver().config
config = Config(**global_config.dict())

# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

eat = on_command("eat", aliases = {'吃啥', '次啥', '恰饭', '干饭了'}, rule=None, priority=2)

@eat.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    msg = event.get_message
    food = choice(
        [
            "今天爷想吃牛筋丸热干面",
            "今天爷想吃牛筋丸炸酱面",
            "今天爷想吃牛腩汤面",
            "今天爷想吃牛腩汤粉",
            "١١(❛ᴗ❛)吃吃吃!!就知道吃",
        ]
    )
    await eat.finish(food)

highperf = on_command("highperf", priority=2)

@highperf.handle()
async def _(bot: Bot, event: Event, state: T_State):
    voice = (
        Path(".")
        / "apeiria_network"
        / "data"
        / "voice"
        / "ATR_b101_013_高性能.wav"
    )
    voice = voice.resolve()
    message_type = str(event.dict()["message_type"])
    if message_type == "group":
        group_id = str(event.dict()["group_id"])
        await bot.call_api("send_group_msg", group_id=group_id, message=f"[CQ:record,file=file:///{voice}]")
    elif message_type == "private":
        user_id = event.get_user_id()
        await bot.call_api(api="send_private_msg", user_id=user_id, message=f"[CQ:record,file=file:///{voice}]")