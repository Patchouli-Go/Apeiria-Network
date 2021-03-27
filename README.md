# Apeiria-Network
基于Nonebot2编写的聊天机器人

## How to start

1. 创建python虚拟环境(可选) 项目根目录键入 `python3 -m venv .venv`
    Linux下激活虚拟环境: `source .venv/bin/activate`
    Windows下激活虚拟环境: `/.venv/Scripts/activate.bat`
2. 安装依赖包 `pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/`
3. 启动bot `nb run`

## 有哪些功能？
1. 天气！
    早上8点自动推送天气信息，要提前绑定所在城市
    使用方式：`天气`就完事了
    还有个`天气预报`预报七日内天气
2. 状态！随手加了个mcs的，除了我应该没人用就是了）
    `状态`
3. 复读）三句复读一句，图片的懒了，没写
    打开开关就是无情的复读机器（`ONrepeat`
4. 开关
    `ON` `OFF`
4. 其它，下面的配置项里面有

## Bot 配置
使用前请填好.env中的可配置项：
带星号为必须

你的qq账号*:
`SUPERUSERS=[""]`

机器人qq号*:
`SELF_ID=''`

天气api key*:
`WEATHER_KEY=''`

1.5小时喝水群号:
`DRINK_WATER=[""]`

每日天气提醒qq号:
`DAILY_WEATHER=[""]`