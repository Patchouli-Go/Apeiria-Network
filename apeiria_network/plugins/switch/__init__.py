# import nonebot

import json

from pathlib import Path

from .config import Config

from nonebot import on_command, get_driver
# from nonebot import drivers, require

from nonebot.permission import SUPERUSER

# from nonebot.rule import to_me

from nonebot.typing import T_State

from nonebot.adapters.cqhttp import Bot, Event

# from apeiria_network.log import logger

global_config = get_driver().config
config = Config(**global_config.dict())

# _sub_plugins = set()
# _sub_plugins |= nonebot.load_plugins(
#     str((Path(__file__).parent / "plugins").
#         resolve()))



# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

# 添加user_id和group_id判断？

def _switch(args, status, event):
    message_type = str(event.dict()['message_type'])
    try:
        if message_type == 'group':
            id = str(event.dict()['group_id'])
            message_type = "on_group"
            message_typec = "群聊"
            switch = Path('.') / 'apeiria_network' / 'config' / args /  'group' /'switch.json'
        elif message_type == 'private':
            id = event.get_user_id()
            message_type = "on_user"
            message_typec = "用户"
            switch = Path('.') / 'apeiria_network' / 'config' / args /  'private' / 'switch.json'
        data = { id: status }
        with open(switch, mode='r', encoding='utf-8') as f:
            switch_reader = json.load(f)
            with open(switch, mode='w', encoding='utf-8') as switch_json_file_w:
                # if args in switch_reader:
                if id in switch_reader:
                    if switch_reader[id] == status:
                        json.dump(switch_reader, switch_json_file_w, ensure_ascii=False, indent=4)
                        return 'Owner，该功能无需开启。'
                else:
                    switch_reader.update(data)
                switch_reader[id] = status
                json.dump(switch_reader, switch_json_file_w, ensure_ascii=False, indent=4)
                if status == 'on':
                    return '已为该'+message_typec+'开启功能'+args
                elif status == 'off':
                    return '已为该'+message_typec+'关闭功能'+args
    except:
        return 'Owner，我没有这个功能。'
            # elif :
            #     switch_reader.update(data)
            # else:
            #     json.dump(switch_reader, switch_json_file_w)
            #     return 'Owner，我没有这个功能。'


switch_on = on_command('ON', rule=None, permission=SUPERUSER, priority=1)


@switch_on.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    # if message_type == 'group':
    #     id = str(event.dict()['group_id'])
    # elif message_type == 'private':
    #     id = event.get_user_id()
    # logger.info(event.get_message())
    # logger.info(args)
    receive = _switch(args, 'on', event)
    await switch_on.finish(receive)


switch_off = on_command('OFF', rule=None, permission=SUPERUSER, priority=1)


@switch_off.handle()
async def _(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    # message_type = str(event.dict()['message_type'])
    # logger.info(event.get_message())
    # logger.info(args)
    receive = _switch(args, 'off', event)
    await switch_on.finish(receive)
