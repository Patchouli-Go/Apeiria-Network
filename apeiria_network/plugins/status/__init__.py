import json
import psutil
from nonebot import get_driver
from .config import Config
from .data_source import request_api_params
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event

global_config = get_driver().config
config = Config(**global_config.dict())
master = global_config.superusers
URL = "http://patchouli-go.cn:23333/api/status/Old_Alices_Pigeon_Life25620"


def formats(num):
    if num > 1073741824.0:
        num /= 1073741824.0
        return str(round(num, 2)) + "GiB"
    if num > 1048576.0:
        num /= 1048576.0
        return str(round(num, 2)) + "MiB"
    if num > 1024.0:
        num /= 1024.0
        return str(round(num, 2)) + "KiB"
    return str(round(num, 2)) + "Byte"


systemStatus = on_command("status", aliases={"状态"}, rule=None, priority=2)


@systemStatus.handle()
async def _(bot: Bot, event: Event, state: T_State):
    s_type = str(event.get_message()).strip()
    print(s_type)
    if s_type == "":
        s_type = "server"
    if s_type == "server" or s_type == "服务器":
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            memoryava = psutil.virtual_memory().available
            memorytot = psutil.virtual_memory().total
            disk = (
                psutil.disk_usage("/").percent + psutil.disk_usage("/home/").percent
            ) * 0.5
            diskava = psutil.disk_usage("/").free + psutil.disk_usage("/home/").free
            disktot = psutil.disk_usage("/").total + psutil.disk_usage("/home/").total
            disk2 = psutil.disk_usage("/mnt/dm-4/").percent
            disk2ava = psutil.disk_usage("/mnt/dm-4/").free
            disk2tot = psutil.disk_usage("/mnt/dm-4/").total
            inteSENT = psutil.net_io_counters().bytes_sent
            inteRECV = psutil.net_io_counters().bytes_recv
        except:
            await systemStatus.finish("请求数据貌似失败了...")
        else:
            status = "アトリは、高性能ですから！"
            if cpu > 80:
                status = "ATRI感觉头有点晕..."
                if memory > 80:
                    status = "ATRI感觉有点头晕并且有点累..."
        if disk > 80:
            if disk2 > 80:
                status = "ATRI感觉身体要被塞满了..."
        msg0 = "ATRI status-info:\n"
        msg0 += "* CPU: " + str(cpu) + "%\n"
        msg0 += "* MEM: " + formats(memoryava) + " / " + formats(memorytot) + "\n"
        msg0 += "* Disk1 " + formats(diskava) + " / " + formats(disktot) + "\n"
        msg0 += "* Disk2 " + formats(disk2ava) + " / " + formats(disk2tot) + "\n"
        msg0 += "* BytesSENT: " + str(inteSENT) + "\n"
        msg0 += "* BytesRECV: " + str(inteRECV) + "\n"
        msg0 += status
        await systemStatus.finish(msg0)
    elif s_type == "mc" or s_type == "MC":
        URL = "http://patchouli-go.cn:23333/api/status/Old_Alices_Pigeon_Life25620"
        status = "UNKNOW"
        dc = json.loads(request_api_params(url=URL, params=""))
        if dc["status"] is True:
            status = "在线"
            sname = dc["motd"]
            sversion = dc["version"]
            curplayers = dc["current_players"]
            maxplayers = dc["max_players"]
        elif dc["status"] is False:
            status = "离线"
            sname = "None"
            sversion = "None"
            curplayers = "0"
            maxplayers = "0"
        msg0 = "周目名:    " + sname + "\n"
        msg0 += "版本号:    " + sversion + "\n"
        msg0 += "服务状态:  " + status + "\n"
        msg0 += "在线人数:  " + curplayers + "/" + maxplayers
        await systemStatus.finish(msg0)
