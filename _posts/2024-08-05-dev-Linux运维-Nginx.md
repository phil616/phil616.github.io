---
layout: post
title: Linux运维-Nginx
categories: [Blog, Devops]
tags: [web]
date: 2024-08-05 23:10 +0800
---
> AUTOGEN dd34db6a2b5a49979c19d1d781fa1cee

# Linux Nginx

## 介绍

Nginx是一个高性能的HTTP和反向代理服务器，同时也提供了IMAP/POP3/SMTP服务。它是由Igor Sysoev创建的，最初是为处理大量并发连接而设计的，因此它在高并发环境下表现出色。下面是Nginx的一些主要功能和使用方式：

Nginx的功能：

1. **静态内容服务**：Nginx可以高效地提供静态内容，如图片、视频、CSS和JavaScript文件等。
2. **反向代理**：Nginx可以作为反向代理服务器，将客户端的请求转发到后端服务器上。
3. **负载均衡**：Nginx可以分配请求到多个后端服务器上，从而实现负载均衡。
4. **SSL终端**：Nginx支持SSL终端，可以处理HTTPS请求，提供加密通信。
5. **缓存**：Nginx可以缓存动态和静态内容，提高响应速度和减少服务器负载。
6. **压缩**：Nginx支持Gzip压缩，可以减少传输数据量，加快页面加载速度。
7. **URL重写**：Nginx可以进行URL重写，实现URL的美化或重定向。
8. **访问控制**：Nginx可以控制访问权限，如限制IP访问等。

如何使用Nginx：

1. **安装Nginx**：根据你的操作系统，可以通过包管理器或源代码编译的方式安装Nginx。
2. **配置Nginx**：Nginx的配置文件通常位于`/etc/nginx/nginx.conf`，你可以编辑这个文件来配置服务器的行为。
3. **启动Nginx**：安装并配置完成后，可以通过命令行启动Nginx服务。
4. **管理Nginx**：使用命令行工具管理Nginx，如重新加载配置文件、查看状态等。
5. **设置虚拟主机**：在Nginx中可以设置多个虚拟主机，每个虚拟主机都有自己的配置。
6. **设置反向代理**：配置Nginx作为反向代理，将请求转发到后端服务器。
7. **设置负载均衡**：配置多个后端服务器，并设置负载均衡策略。
8. **优化性能**：根据需要调整Nginx的配置，如调整缓冲区大小、连接超时等，以优化性能。

Nginx的使用相对简单，但要充分利用其功能，可能需要对配置文件进行深入的学习和调整。

## 本地安装

在Linux上安装Nginx通常有几种方法，包括使用包管理器、从源代码编译以及使用Nginx的官方仓库。以下是一些常见Linux发行版上安装Nginx的基本步骤：

## 1. apt

对于基于Debian的系统（如Ubuntu）：

1. 更新包索引：
   ```bash
   sudo apt update
   ```

2. 安装Nginx：
   ```bash
   sudo apt install nginx
   ```

3. 启动Nginx服务：
   ```bash
   sudo systemctl start nginx
   ```

4. 检查Nginx状态：
   ```bash
   sudo systemctl status nginx
   ```

5. 允许Nginx通过防火墙（如果使用ufw）：
   ```bash
   sudo ufw allow 'Nginx HTTP'
   ```

## 2. rpm

对于基于RPM的系统（如CentOS或Fedora）：

1. 安装EPEL仓库（如果尚未安装）：
   ```bash
   sudo yum install epel-release
   ```

2. 安装Nginx：
   ```bash
   sudo yum install nginx
   ```

3. 启动Nginx服务：
   ```bash
   sudo systemctl start nginx
   ```

4. 检查Nginx状态：
   ```bash
   sudo systemctl status nginx
   ```

5. 允许Nginx通过防火墙（如果使用firewalld）：
   ```bash
   sudo firewall-cmd --permanent --add-service=http
   sudo firewall-cmd --reload
   ```

## 3. 从源码

从源代码编译安装：

1. 安装编译Nginx所需的工具和库：
   ```bash
   sudo apt install build-essential libpcre3 libpcre3-dev zlib1g-dev libssl-dev
   ```

2. 下载最新的稳定版Nginx源代码：
   ```bash
   wget http://nginx.org/download/nginx-版本号.tar.gz
   ```

3. 解压源代码包：
   ```bash
   tar -zxvf nginx-版本号.tar.gz
   ```

4. 进入源代码目录并配置编译选项：
   ```bash
   cd nginx-版本号
   ./configure
   ```

5. 编译并安装Nginx：
   ```bash
   make
   sudo make install
   ```

6. 配置Nginx（如果需要）并启动服务。

## 4. 使用官方仓库

使用Nginx官方仓库：

1. 添加Nginx官方GPG密钥：
   ```bash
   wget https://nginx.org/keys/nginx_signing.key
   sudo apt-key add nginx_signing.key
   ```

2. 添加Nginx存储库：
   ```bash
   echo "deb https://nginx.org/packages/debian/ $(lsb_release -cs) nginx" | sudo tee /etc/apt/sources.list.d/nginx.list
   ```

3. 更新包索引并安装Nginx：
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

安装完成后，你可以通过浏览器访问`http://your_server_ip`来测试Nginx是否成功安装并运行。如果一切正常，你应该能看到Nginx的默认欢迎页面。

## Docker安装

要安装并配置Nginx在Docker中，您可以按照以下步骤进行操作：

1. 安装Docker：
   - 在您的操作系统上安装Docker。可以根据您的操作系统类型（如Windows、macOS或Linux）参考Docker官方文档进行安装。

2. 拉取Nginx镜像：
   - 打开终端或命令提示符，运行以下命令来拉取Nginx Docker镜像：

     ```
     docker pull nginx
     ```

   这将从Docker Hub上下载最新版本的Nginx镜像。

3. 创建Nginx容器并配置网络环境：
   - 运行以下命令来创建一个新的Nginx容器，并将主机的端口映射到容器的端口：

     ```
     docker run --name mynginx -p 80:80 -d nginx
     ```

   这将创建一个名为`mynginx`的容器，并将主机的80端口映射到容器的80端口。您可以根据需要修改端口映射规则。

4. 使用Nginx配置：
   - 要使用自定义的Nginx配置文件，您可以将配置文件复制到容器内部的适当位置。首先，创建一个用于存储Nginx配置文件的目录：

     ```
     mkdir nginx-config
     ```

   - 将您的Nginx配置文件（例如`nginx.conf`）复制到该目录中。

   - 然后，将配置文件挂载到Nginx容器中。运行以下命令：

     ```
     docker run --name mynginx -p 80:80 -v /绝对路径/nginx-config:/etc/nginx/conf.d -d nginx
     ```

     将`/绝对路径/nginx-config`替换为您刚才创建的目录的绝对路径。

     这将把您的配置文件挂载到容器中的`/etc/nginx/conf.d`目录，Nginx将使用该目录中的配置。

   - 重新启动容器以使配置生效：

     ```
     docker restart mynginx
     ```

   现在，您的自定义配置将在Nginx容器中生效。

# 安装拓展插件

### Nginx 的拓展插件

Nginx 是一个高性能的 HTTP 和反向代理服务器，也可以用作邮件代理服务器。它的功能通过各种模块来扩展，有些是自带的，有些则通过第三方模块实现。这些模块可以增强 Nginx 的功能，比如增加对 Web 应用的支持、提高安全性、优化性能等。

### 常见的 Nginx 第三方模块：

1. **ngx_pagespeed** - 由 Google 开发，用于自动优化网站资源，如压缩 CSS、JS 文件，优化图片等。
2. **ModSecurity** - 提供 Web 应用防火墙 (WAF) 功能，增加安全性。
3. **Nginx Cache Purge** - 允许通过 Nginx 清除缓存的 URL。
4. **ngx_http_substitutions_filter_module** - 用于执行响应内容的替换。
5. **ngx_brotli** - Google 开发的 Brotli 压缩算法的支持，用于更高效的内容压缩。
6. **Nginx RTMP Module** - 支持 RTMP 和 HLS 直播流。
7. **Lua nginx module** - 为 Nginx 添加 Lua 脚本支持，非常灵活，可以在 Nginx 中直接运行 Lua 脚本。

### 如何安装 Nginx 模块：

Nginx 的模块安装通常需要在 Nginx 编译阶段进行，因为大多数模块需要与 Nginx 一起编译，尤其是第三方模块。以下是一般的安装步骤：

1. **下载 Nginx 源代码**：
   
   ```bash
   wget http://nginx.org/download/nginx-1.18.0.tar.gz
   tar -xzvf nginx-1.18.0.tar.gz
   cd nginx-1.18.0/
   ```

2. **下载所需的模块源代码**：
   
   以 `ngx_pagespeed` 为例：

   ```bash
   cd ..
   git clone https://github.com/apache/incubator-pagespeed-ngx.git ngx_pagespeed
   cd ngx_pagespeed
   # 根据模块的安装指南获取依赖
   wget https://dl.google.com/dl/page-speed/psol/1.13.35.2-x64.tar.gz
   tar -xzvf 1.13.35.2-x64.tar.gz
   ```

3. **编译 Nginx 与模块**：

   返回到 Nginx 源代码目录，并开始编译，加入 `--add-module` 参数指向模块的源代码目录：

   ```bash
   cd ../nginx-1.18.0/
   ./configure --add-module=../ngx_pagespeed
   make
   sudo make install
   ```

4. **配置模块**：

   编译安装后，需要在 Nginx 的配置文件中添加相应的配置项来启用和配置模块。

   例如，对于 `ngx_pagespeed`，可能需要添加：

   ```nginx
   pagespeed on;
   pagespeed FileCachePath /var/ngx_pagespeed_cache;
   ```

5. **重启 Nginx**：

   ```bash
   sudo nginx -s reload
   ```

### 注意事项

- 安装第三方模块可能会增加 Nginx 的复杂性和维护难度，确保在生产环境中充分测试。
- 一些模块可能不兼容最新版本的 Nginx，需要检查模块的兼容性。
- 安全性和性能也需要在引入新模块后重新评估。



# 配置规则

Nginx 配置文件通常是 `nginx.conf`，位于 `/etc/nginx/` 或 `/usr/local/nginx/conf/` 目录下。配置文件使用简洁的结构性语法，包括指令（directives）和块（blocks 或 contexts）。

## 基本语法规则：

- 指令以分号 (`;`) 结束。
- 块用花括号 (`{}`) 包围，可以包含其他指令或子块。
- 配置文件中的每一行应该包含一个指令或一个块的开始/结束。
- 注释用井号 (`#`) 开始，持续至行尾。

## 基本关键字（contexts）：

- **main**: 全局设置，影响整个 Nginx 服务器。
- **events**: 控制 Nginx 服务器与客户端之间的网络连接。
- **http**: 配置 HTTP 服务器的功能，如服务器列表和各种 HTTP 选项。
- **server**: 定义服务器的具体配置，通常包括监听的 IP 地址、端口以及虚拟主机的详细配置。
- **location**: 定位请求的特定 URL，并定义如何处理这些请求。

### 1. 配置反向代理

**反向代理** 的配置示例：

```nginx
http {
    server {
        listen 80;
        server_name example.com;

        location / {
            proxy_pass http://localhost:3000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
```

这个配置使得 Nginx 监听端口 80 并将所有到 `example.com` 的 HTTP 请求转发到本地的 3000 端口。

### 2. 配置安全规则

**限制 IP 访问** 的配置示例：

```nginx
http {
    server {
        listen 80;
        server_name example.com;

        location /admin {
            allow 192.168.1.100;
            deny all;
        }
    }
}
```

此配置仅允许 IP 地址为 `192.168.1.100` 的用户访问 `/admin` 路径，其他所有访问都被拒绝。

### 3. 配置 SSL

**SSL 配置** 用于启用 HTTPS：

```nginx
http {
    server {
        listen 443 ssl;
        server_name example.com;

        ssl_certificate /etc/ssl/certs/example.com.crt;
        ssl_certificate_key /etc/ssl/private/example.com.key;

        ssl_session_cache shared:SSL:1m;
        ssl_session_timeout 10m;

        ssl_ciphers 'HIGH:!aNULL:!MD5';
        ssl_prefer_server_ciphers on;

        location / {
            root /usr/share/nginx/html;
            index index.html index.htm;
        }
    }
}
```

此配置使 Nginx 通过 443 端口接收 HTTPS 请求，并使用指定的证书和密钥。此外，还配置了 SSL 会话缓存和超时设置，以及安全密码套件。
