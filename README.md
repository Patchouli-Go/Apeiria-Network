# Apeiria-Network
基于Nonebot2编写的聊天机器人

## How to start

1. 创建python虚拟环境(可选) `python3 -m venv .venv`
    `source .venv/bin/activate` (激活虚拟环境)
2. 安装环境 `pip install -r requirements.txt`
3. 启动bot `nb run`

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