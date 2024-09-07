---
layout: post
title: 使用CloudFlare进行代理
categories: [Blog, Devops]
tags: [memo,project,web]
date: 2024-09-07 22:00 +0800
---
> AUTOGEN 64eccd15a8aa40549b1abfae91b0ea58

# 使用Cloudlare的Worker进行网络代理

1. 使用库

https://github.com/jonssonyan/cf-workers-proxy

2. 创建Worker
3. 保存并上线
4. 在Worker应用 - 设置 - 触发器 - 自定义域名中添加一个域名 
5. 在Worker应用 - 设置 - 变量 - 设置`PROXY_HOSTNAME`变量为自有地址，例如`registry-1.docker.io`
6. 使用如下配置使Worker生效

```
mkdir -p /etc/docker
cat >/etc/docker/daemon.json <<EOF
{
  "registry-mirrors":["https://dockerhub.xxx.com"]
}
EOF
systemctl daemon-reload
systemctl restart docker
```

详见代理配置库
