---
layout: post
title: Linux-连接OpenVPN服务
categories: [Blog, Devops]
tags: [project]
date: 2024-09-04 13:23 +0800
---
> AUTOGEN b2f50fe4e24244279d1b07a3f42e098a

# Linux下使用OpenVPN连接服务器

1. 安装OpenVPN

   ```bash
   sudo apt update
   sudo apt install openvpn
   ```

2. 获取ovpn配置文件

   ```
   scp user@server:config.ovpn /etc/openvpn
   ```

## 直接连接

```bash
sudo openvpn --config /etc/openvpn/vmuser.ovpn
```

## 自动连接

创建服务单元

```
sudo vim /etc/systemd/system/vmuser.service
```

使用service

```
[Unit]
Description=OpenVPN connection for vmuser

[Service]
Type=simple
ExecStart=/usr/sbin/openvpn --config /etc/openvpn/vmuser.ovpn
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

启用服务

```
sudo systemctl enable vmuser.service
sudo systemctl start vmuser.service
```

停止服务

```
sudo systemctl stop vmuser.service
```

![image-20240904132657002](../assets/img/2024-09-04-dev-Linux-连接OpenVPN服务/image-20240904132657002.png)
