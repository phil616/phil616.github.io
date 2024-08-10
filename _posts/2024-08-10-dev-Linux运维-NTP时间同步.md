---
layout: post
title: Linux运维-NTP时间同步
categories: [Blog, Devops]
tags: [web]
date: 2024-08-10 21:01 +0800
---
> AUTOGEN 100a43ad8cbc427792c21cf29ce500cc

# Linux - NTP时间同步

## 时区

时区是地球上根据经度划分的区域，每个区域内的时间相同。由于地球自转，不同经度的地方会有不同的日出和日落时间。为了统一时间，国际上将地球划分为24个主要时区，每个时区覆盖15度经度。每个时区的时间比前一个时区早或晚1小时（有些时区是半小时或四分之一小时的偏差，以适应国家或地区的具体需要）。

标准的世界时区图如下：

![image-20240810210441533](../assets/img/2024-08-10-dev-Linux%E8%BF%90%E7%BB%B4-NTP%E6%97%B6%E9%97%B4%E5%90%8C%E6%AD%A5/image-20240810210441533.png)

可以利用如下的Python代码打印所有地区的基于UTC时间的偏移量：

```py
import pytz
from datetime import datetime

# Get the current time
now = datetime.now()

# Iterate through all timezones
for timezone in pytz.all_timezones:
    tz = pytz.timezone(timezone)
    offset = tz.utcoffset(now)
    offset_hours = int(offset.total_seconds() // 3600)
    offset_minutes = int((offset.total_seconds() % 3600) // 60)
    sign = '+' if offset_hours >= 0 else '-'
    offset_str = f"UTC{sign}{abs(offset_hours):02}{abs(offset_minutes):02}"
    print(f"{timezone}: {offset_str}")
```

例如

```text
...
Asia/Omsk: UTC+0600
Asia/Oral: UTC+0500
Asia/Phnom_Penh: UTC+0700
Asia/Pontianak: UTC+0700
Asia/Pyongyang: UTC+0900
Asia/Qatar: UTC+0300
Asia/Qostanay: UTC+0600
Asia/Qyzylorda: UTC+0500
Asia/Rangoon: UTC+0630
Asia/Riyadh: UTC+0300
Asia/Saigon: UTC+0700
Asia/Sakhalin: UTC+1100
Asia/Samarkand: UTC+0500
Asia/Seoul: UTC+0900
Asia/Shanghai: UTC+0800
Asia/Singapore: UTC+0800
Asia/Srednekolymsk: UTC+1100
Asia/Taipei: UTC+0800
Asia/Tashkent: UTC+0500
Asia/Tbilisi: UTC+0400
Asia/Tehran: UTC+0330
...
```

## 时间标准

1. **协调世界时（UTC）**：是目前全球通用的时间标准，由原子钟提供，以秒为单位的时间计量系统。UTC通过添加闰秒以保持与地球自转周期一致，其误差值必须保持在0.9秒以内。

2. **国际原子时（TAI）**：基于铯-133原子的振荡周期，是连续性时标，准确度极高，每日误差仅为数纳秒。

3. **世界时（UT）**：基于地球自转的时间计量系统，由于地球自转速度的不均匀性，它是一个非均匀时间系统。世界时有多个版本，包括UT0（未修正的世界时）、UT1（考虑了极移改正的世界时）和UT2（进一步考虑季节性变化的世界时）。

4. **格林尼治标准时间（GMT）**：历史上作为世界时间标准，基于太阳经过格林尼治子午线的时间，但由于地球自转的不均匀性，已不再作为标准时间使用。

5. **本地时间（LT）**：指某一特定时区内的时间，由与UTC之间的偏移量来定义。例如，北京时间就是东八区的本地时间，即UTC+8。

6. **夏令时（DST）**：一些国家和地区为了节约能源而实行的时间制度，在夏季将时间调快一小时。不同国家和地区的夏令时开始和结束时间不同。

此外，还有基于地球自转的恒星时和平太阳时，它们分别对应于地球相对于恒星和太阳的位置。而北京时间是中国统一使用的标准时间，即UTC+8时区的时间。

额外介绍：

[手机电脑是怎么“对表”的？_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1gt421A7GR/)

## chrony

Chrony是一个开源的网络时间协议（NTP）客户端和服务器软件，用于保持计算机系统时钟的精确同步。它由两个主要程序组成：`chronyd`和`chronyc`。`chronyd`是一个后台守护进程，负责调整系统时钟与时钟服务器同步，而`chronyc`提供了一个用户界面，用于监控性能和进行配置。

Chrony的优势包括快速同步、高精度、低资源占用和良好的网络环境适应性。它可以在几分钟内实现系统时钟的同步，适用于不稳定和高延迟的网络环境，并且在节能技术导致的时钟频率变化下也能保持稳定。

Chrony适用于需要精确时间同步的场景，例如分布式系统，它可以确保所有服务使用相同的时间，避免时间偏差引发的问题。在Red Hat Enterprise Linux 8中，Chrony默认安装，可以通过`systemctl`命令来管理服务，并使用`chronyc`命令检查同步状态和进行手动调整。

Chrony的基本原理包括选择时钟源、测量延迟和偏差、计算时钟校正以及调整系统时钟。它使用时钟滤波器算法进行同步，通过对时间样本进行加权平均来提高准确性。

## 注意

1. chrony只有在RedHat中为默认安装，其它情况都需要先联网安装
2. chrony更改时间时为跳变，建议先配置好后再启动服务
3. chrony如果在联网情况下安装则会自动使用默认的网络时钟服务器

# chrony安装

1. 安装

```
sudo apt install chrony -y
```

```
systemctl enable --now chronyd
```

```
sudo service chrony start
```

2. 查看当前的同步源

```
chronyc sources
```

![image-20240810212840466](../assets/img/2024-08-10-dev-Linux%E8%BF%90%E7%BB%B4-NTP%E6%97%B6%E9%97%B4%E5%90%8C%E6%AD%A5/image-20240810212840466.png)

注意签名的MS表示的是源的状态

```text
状态的情况如下：
* 表示当前同步的源
+ 表示可选的时间源
- 表示被组合算法排除的时间源
? 表示链接已丢失或是数据包未通过测试的时间源
x 表示虚假的时间源，它的时间和其它源不一致
~ 表示该时间源有太多可变性的来源
```

## 为chrony配置时间服务器

在`/etc/chrony/chrony.conf`中可以更改ntp源，时间服务器等

![image-20240810213502824](../assets/img/2024-08-10-dev-Linux%E8%BF%90%E7%BB%B4-NTP%E6%97%B6%E9%97%B4%E5%90%8C%E6%AD%A5/image-20240810213502824.png)

