---
layout: post
title: Github用户内容站CDN加速
categories: [Blog, Tips]
tags: [tech]
date: 2024-11-11 21:46:05 +0800
---
> AUTOGEN: b47dbe31f4af402f8be6f4ecf3ab0f8b

# Github用户内容站CDN加速

PicGO上传后，部分内容无法被大陆地区访问，因此使用cloudflare进行cdn代理。

例如下面的内容

https://raw.githubusercontent.com/phil616/phil616.assets/main/phil616_picgo/image-20241107194511953.png

源站为`raw.githubusercontent.com/phil616/`使用域名加速

assets.phil616.greenshadecapital.com

## 1.创建代理

使用

https://github.com/jonssonyan/cf-workers-proxy

创建一个worker代理

增加下面的域名

| K             | V                                   |
| ------------- | ----------------------------------- |
| Custom domain | docker.mirror.greenshadecapital.com |

## 2. 增加变量

| Type      | Name             | Value      |      |
| --------- | ---------------- | ---------- | ---- |
| Plaintext | `PATHNAME_REGEX` | ^/phil616/ |      |

```
PROXY_HOSTNAME = raw.githubusercontent.com
```

## 3.配置PicGo

https://assets.phil616.greenshadecapital.com

验证可行性

https://raw.githubusercontent.com/phil616/phil616.assets/main/phil616_picgo/image-20241111213733389.png

![image-20241111214221139](https://assets.phil616.greenshadecapital.com/phil616/phil616.assets/main/phil616_picgo/image-20241111214221139.png)

需要设置为：

https://assets.phil616.greenshadecapital.com/phil616/phil616.assets/main

再次验证

![image-20241111214320168](https://assets.phil616.greenshadecapital.com/phil616/phil616.assets/main/phil616_picgo/image-20241111214320168.png)
