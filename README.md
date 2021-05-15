# Apeiria-Network

基于 Nonebot2 编写的聊天机器人
编写环境：Centos8.3 Python3.8.8
没有在windows上测试过，如有bug，还请体谅

## How to start

### 对于初次使用 Nonebot2 框架的用户：

1. 创建 python 虚拟环境(可选) 项目根目录键入 `python3 -m venv .venv`  
   Linux 下激活虚拟环境: `source .venv/bin/activate`  
   Windows 下激活虚拟环境: `/.venv/Scripts/activate.bat`  
2. 安装依赖包 `pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/`
3. 启动 bot `nb run`
      需要额外安装redis

为配合 Nonebot2 使用，还需要安装搭建 Go-Cqhttp 使用：https://github.com/Mrs4s/go-cqhttp  
这是我的个人博客：http://blog.patchouli-go.cn:8109/?p=57

### 你事老手？
（屎山，球放过）  
安装依赖包 `pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/`  
启动 bot `nb run`

## 有哪些功能？

1. 天气！  
   早上 8 点自动推送天气信息，要提前绑定所在城市  
   使用方式：`天气`就完事了  
   还有个`天气预报`预报七日内天气
2. 状态！随手加了个 mcs 的，除了我应该没人用就是了）  
   `状态`
3. 俄罗斯转盘  
   输入`开枪`或者`开枪 子弹数量`初始化  
   后续输入`开枪`进行游戏
4. 复读）三句复读一句，图片的懒了，没写  
   打开开关就是无情的复读机器（`ONrepeat`
5. 开关  
   `ON` `OFF`
6. 其它，下面的配置项里面有  

## Bot 配置

使用前请填好.env 中的可配置项：  
带星号为必须  

你的 qq 账号\*:  
`SUPERUSERS=[""]`

机器人 qq 号\*:  
`SELF_ID=''`

天气 api key\*:  
`WEATHER_KEY=''`

1.5 小时喝水群号:  
`DRINK_WATER=[""]`

每日天气提醒 qq 号:  
`DAILY_WEATHER=[""]`

懂？:  
`apikey_LOLI=''`