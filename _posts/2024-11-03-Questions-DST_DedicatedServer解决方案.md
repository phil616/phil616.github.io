---
layout: post
title: DST_DedicatedServer解决方案
categories: [Blog, Questions]
tags: [project]
date: 2024-11-03 21:46:05 +0800
---
> AUTOGEN: 62f38c8a8222414881c5b62032b58994

# DST_DedicatedServer解决方案

# DST内网穿透方案

## 0. 介绍

本方案使用`frp` + 公网服务器 + 本地机器服务器

介绍，饥荒联机版可使用官方服务器，也可以使用专用服务器，本文档介绍了一种通过内网传统来搭建饥荒联机版专用服务器的方法。

饥荒联机版的架构是，科雷官方拥有一台索引服务器，用于存储支持游戏运行的服务器的索引信息，玩家可以在浏览游戏中看到所有索引信息。

专用服务器在启动服务器后，需要向索引服务器发送信息，这样玩家才能够在游戏大厅中搜索到服务器（房间）。

## 1. 准备内网穿透

使用frp进行内网穿透。https://github.com/fatedier/frp

### 1.1 服务端设置

配置`frps.toml`

```
# 绑定TCP7000端口
bindPort = 7000
auth.token = "客户端连接服务器的token"
# 管理页面
webServer.addr = "0.0.0.0"
webServer.port = 8888
webServer.user = "admin"
webServer.password = "服务器密码"
```

额外的`systemd`文件

```
[Unit]
Description=frps service
After=network.target

[Service]
Type=simple
ExecStart=/root/frp/frps -c /root/frp/frps.toml
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
```

可以使用systemd来自动启动服务器

```bash
systemctl enable frps.service
systemctl start frps.service
```

查看状态

```bash
systemctl status frps.service
```

也可以通过Web界面进行查看。

### 1.2 客户端设置

在Windows客户端中，配置`frpc.toml`

```
# frpc.toml
# 服务器地址和认证信息
serverAddr = "39.101.195.189"
serverPort = 7000
auth.token = "Carvinte055432"

# 代理UDP 10086 端口为主世界
[[proxies]]
name = "dts_master"
type = "udp"
localIP = "127.0.0.1"
localPort = 10086
remotePort = 10086

# 代理洞穴
 [[proxies]]
name = "dts_caves"
type = "udp"
localIP = "127.0.0.1"
localPort = 10087
remotePort = 10087
```

洞穴和主世界分别使用两个不同的UDP端口

## 2. 制作存档

存档的制作是在游戏内完成的，在游戏中新建世界后，会生成存档。打开游戏，创建游戏-配置规则-生成新世界

### 2.1 制作本地存档

打开游戏，打开新建的世界管理-打开世界文件夹，获取Cluster开头的文件夹内容，应该有

* Master文件夹-主世界文件夹
* Caves文件夹-洞穴文件夹
* cluster.ini服务器配置

将存档另存，并进行修改

### 2.2 更新信息

需要更新的信息有

* **cluster_token.txt**

打开游戏 - 账号 - 导航栏游戏 - 《饥荒：联机版》的游戏服务器，添加新服务器，并获得服务器票据。该票据是索引服务器的唯一标识。

* Master/server.ini

```
[NETWORK]
server_port = 10999
```

更改server_port 为主世界的UDP端口

* Caves/server.ini

```
[NETWORK]
server_port = 10999
```

更改server_port为洞穴的UDP端口

* adminlist.txt

可有可无，里面是管理员列表，可以使用控制台，ID从账户 - 用户信息 - Klei用户ID获取

## 3. 应用存档信息

将存档放入`C:\Users\Astar\Documents\Klei\DoNotStarveTogether`文件夹内

该文件夹下应该有

* USERID - Steam用户的文件夹，里面存储着Steam用户的个人游戏存档
* backup - 日志备份 可选
* Cluster_1 - 服务器存档，可能是其他的存档
* 其他日志文件

## 4. 配置服务器信息

打开Steam，选择库-工具-Don't Starve Together Dedicated Server - 设置 - 管理 - 浏览本地文件

打开`bin/scripts`

### 4.1 配置本地服务器

本地服务器的配置信息需要更改，修改`launch_preconfigured_servers.bat`文件中的内容

```
@ECHO OFF

set SteamAppId=322330
set SteamGameId=322330

cd ..
start "Don't Starve Together Overworld" /D "%~dp0.." "%~dp0..\dontstarve_dedicated_server_nullrenderer.exe" -cluster Cluster_2 -console -shard Master
start "Don't Starve Together Caves"     /D "%~dp0.." "%~dp0..\dontstarve_dedicated_server_nullrenderer.exe" -cluster Cluster_2 -console -shard Caves
```

即把每个服务器的启动参数改为`-cluster Cluster_2 -console -shard Caves`

其中`Cluster_2`是存档文件夹的名称

## 4.2 启动MOD

在Master和Caves中使用脚本来置换MOD

在Master文件夹中启动

```bash
@echo off
setlocal enabledelayedexpansion
if exist modoverrides.lua  (
	echo 正在去除无用信息,并保存至临时文件...
	echo.
   	for /f %%i in (modoverrides.lua) do (
		echo %%i|findstr workshop >> 临时文件.txt
	)
	echo 去除成功,正在提取mod编号并保存至新文件...
	echo.
	for /f %%i in (临时文件.txt) do (
		set str=%%i
		set str1=!str:["workshop-=!
		set str2=!str1:"]=!
		set str3="!str2:~0,-2!"
		echo ServerModSetup(!str3!^)>> dedicated_server_mods_setup.lua
	)
	echo 生成成功！
	echo.
	echo 删除临时文件
	del 临时文件.txt
	echo.
	echo 成功！生成的文件在代码同目录下,替换至游戏目录mods文件夹下即可
	echo.
)  else (
	echo.
    echo 文件不存在,请将代码和modoverrides.lua文件放一起
	echo.
)
pause


rem                                                        --by橙之刃2119820756
```

获得全新的`dedicated_server_mods_setup.lua`替换掉`***\Steam\steamapps\common\Don't Starve Together Dedicated Server\mods`文件夹中的文件

其原理是将存档内的`modoverrides.lua`MOD信息放到服务器中，让服务器加载相关MOD

Master和Caves共享一个MOD列表，因此无需对其进行

在启动服务器后，可能需要下载MOD，提示为

```
...
[00:00:03]: [Workshop] DownloadPublishedFile [8] 2795130977
[00:00:03]: [Workshop] DownloadPublishedFile [8] 2901979304
[00:00:03]: [Workshop] DownloadPublishedFile [8] 2950481491
[00:00:03]: [Workshop] DownloadPublishedFile [8] 3022902813
[00:00:03]: [Workshop] DownloadPublishedFile [8] 3202818257
[00:00:03]: [Workshop] DownloadPublishedFile [8] 3311469531
[00:00:03]: [Workshop] DownloadPublishedFile [8] 351325790
[00:00:03]: [Workshop] DownloadPublishedFile [10] 354533909
[00:00:03]: [Workshop] DownloadPublishedFile [10] 362175979
[00:00:03]: [Workshop] DownloadPublishedFile [10] 363112314
...
```

## 关于MOD

https://developer.valvesoftware.com/wiki/SteamCMD#Windows

https://gitee.com/CHUCHEER/script/raw/master/mod.sh

```
workshop_download_item 322330 
```

## 关于存档

## 关于MOD下载

## 5. 启动服务器

## 5.1 启动内网穿透

```bash
frpc -c frpc.toml
```

若启动成功，则会提示` incoming a new work connection`并进入循环

若启动失败，则会退出。可能的原因：

* 端口占用，使用`netstat -ano | findstr "端口号"`找到相关PID并kill，使用`taskkill /pid xxxx /f`
* 密钥不正确，进入Web管理页面或更改服务端密钥配置
* 云服务器的安全组或出入站点规则限制
* 防火墙未放行

## 5.2 启动服务器

通过启动`launch_preconfigured_servers.bat`来启动服务器

服务器控制台的Master会先提示`Sim paused`随后等待Caves分片服务器同步，Caves也会随后提示`Sim paused`

# 使用管理面板

https://github.com/carrot-hu23/dst-admin-go

Release:
https://github.com/carrot-hu23/dst-admin-go/releases/download/1.3.1/dst-admin-go.1.3.1.tgz

frp:
https://github.com/fatedier/frp/releases/download/v0.61.0/frp_0.61.0_linux_amd64.tar.gz

使用管理面板的方案依然可行，但模组下载和加载过慢的问题无法解决。

