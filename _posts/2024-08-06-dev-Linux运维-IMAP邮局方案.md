---
layout: post
title: Linux运维-IMAP邮局方案
categories: [Blog, Devops]
tags: [web]
date: 2024-08-06 22:15 +0800
---
> AUTOGEN 849cb486f4194c389666a0ba817d5e46

# Linux 邮件服务器

# 1. 介绍

SMTP全称是Simple Mail Transfer Protocol,即简单邮件传输协议。与POP3和IMAP主要用于邮件接收不同,SMTP协议主要用于发送和中转电子邮件。它是一组用于从源地址到目的地址传输邮件的规范,规定了邮件的发送过程和相关的命令。
SMTP协议的主要工作流程如下:

1. 建立连接:邮件客户端(或者发送邮件的服务器)通过SMTP连接到邮件服务器。
2. 握手:客户端和服务器交换一些初始命令,确认身份,说明将要进行邮件发送操作。
3. 发送邮件:客户端提供发件人地址,一个或多个收件人地址,以及邮件内容。这些信息通过一系列SMTP命令发送给服务器。
4. 中转邮件:如果收件人地址不是本服务器管理的,服务器会尝试将邮件中转给管理该地址的服务器。
5. 送达邮件:当邮件到达目标服务器后,如果该地址有效,邮件将被放入该用户的邮箱。
6. 关闭连接:一旦邮件发送完毕,客户端发送QUIT命令,关闭与服务器的连接。

SMTP的一些主要特点包括:

1. 纯文本协议:SMTP是一种基于文本的协议,所有的命令和响应都是纯文本格式。这使得SMTP简单易懂,但也限制了它的功能。
2. 支持附件:通过MIME(Multipurpose Internet Mail Extensions)扩展,SMTP可以支持发送二进制文件,如图片、音频等作为邮件附件。
3. 安全扩展:现代SMTP服务器通常支持SSL/TLS加密,以保护邮件内容不被窃听。此外还有一些认证机制如SMTP AUTH,以防止未经授权的邮件发送。
4. 可靠性:SMTP有一些内置的可靠性机制,如重试发送失败的邮件,发送状态通知等。

# 2. iRedMail

1. 服务器

```
telnet smtp.qq.com 25
```

如果一直超时则说明不可用

```shell
Trying 14.17.57.241...
telnet: connect to address xxx.xxx.xxx.xxx: Connection timed out
Trying 14.18.245.164...
telnet: connect to address xxx.xxx.xxx.xxxo: Connection timed out
```

成功可用的案例：

```shell
Trying 240e:ff:f100:8019::6a...
Connected to smtp.qq.com.
Escape character is '^]'.
220 newxmesmtplogicsvrszc5-0.qq.com XMail Esmtp QQ Mail Server.
```

      1. 允许rDNS - PTR反向代理
      2. 独立IP
      3. 开放25端口
   4. 域名可用
      1. 可更改DNS服务商
      2. 二级域名，例如example.com
   5. iRedMail支持的服务器
         1. 推荐Ubuntu LTS
         2. Centos7不再支持，Centos8停止维护

# 2. 准备工作

## 2.1 设置主机名

为服务器设置一个完整域名（FQDN）的主机名
不管你的服务器将用于实际运行还是仅仅用作测试，都建议设置一个完整域名（FQDN）的主机名。
输入命令 `hostname -f` 查看当前的主机名
假设你的域名为：abc.com
那么你需要将`hostname` 设置为 `mx.abc.com`

```
$ hostname -f
mx.example.com
```

这一步需要再主机上修改两个文件：

1. 修改`/etc/hostname`

命令如下：

```shell
vim /etc/hostname
```

```shell
vim /etc/hostname
#按下 i 进入编辑模式
#删除原有的内容，填入 mx.example.com
mx.example.com
#修改完后，按下 esc,输入 :wq  指令，保存并退出
```

确保hostname只有一行

```latex
mx.example.com
```

## 2.2 更改hosts

定义主机名和 IP 地址的对应关系，注意：一定要将 FQDN 主机名列在第一个

```shell
vim /etc/hosts
#一般来说修改第一行为
127.0.0.1 mx.example.com mx localhost localhost.localdomain
```

修改完毕后，一般需要重启系统生效

```shell
sudo systemctl reboot
#重新检查 hostname -f
hostname -f
```

期望出现mx.example.com

## 2.3 禁用 SELinux

> SELinux是Security-Enhanced Linux的缩写,是一种强制访问控制(MAC)的安全机制。它在Linux内核中提供了更精细和灵活的安全策略,可以严格控制进程、文件、网络端口等系统资源的访问。主要特点包括:
>
> 1. 每个进程和系统资源都有安全上下文(security context),规定了它们的访问权限。
> 2. 使用最小权限原则,即进程只能访问完成其任务所需的最少资源。这限制了系统的攻击面。
> 3. 强制实施安全策略,即使是root用户也受限制,减少误操作和提权风险。
> 4. 支持不同的安全策略,如targeted、mls等,适应不同安全需求。
> 5. 提供审计功能,可以记录违反安全策略的行为,便于事后追查。

iRedMail 不支持 SELinux，所以需要在 `/etc/selinux/config` 文件里禁用它。
删除和禁用SELinux的步骤：

- 查看当前的SELinux状态，运行：`sestatus`
- ![image-20240806221950390](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806221950390.png)
- 编辑 `vim /etc/selinux/config`文件，并将'SELINUX'设置为`disabled'。

```shell
SELINUX=disabled
```

- 重启Linux服务器 `sudo reboot`
- 运行`sestatus`检查selinux状态
- ![image-20240806222106516](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806222106516.png)

```
SElinux status     disabled
```

# 3. 安装iRedMail

截止到2024.7.31最新的iRedMail为1.7.0

```shell
cd /root/
wget https://github.com/iredmail/iRedMail/archive/refs/tags/1.7.0.tar.gz
#因为我上面下载的是1.6.3.tar.gz，这里解压 1.6.3.tar.gz
tar zxf 1.7.0.tar.gz
```

![image-20240806222132583](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806222132583.png)



3.1 启动安装程序

```
cd iRedMail-1.7.0

bash iRedMail.sh
```

3.2 允许"Universe"和"Multiverse" 软件源

![image-20240806223006994](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806223006994.png)

3. 3安装过程截图

允许安装

![image-20240806223151564](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806223151564.png)

收件箱目录

![image-20240806223201742](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806223201742.png)

代理服务

![image-20240806223210590](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806223210590.png)

后端数据库选择，Maria DB兼容MySQL

![image-20240806223226878](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806223226878.png)

MySQL root密码

![image-20240806223241704](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806223241704.png)

设置邮件管理员的密码

发件域名

![image-20240806223304732](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806223304732.png)

辅助组件可选的组件(默认即可)

- Roundcubemail — 网页邮件客户端
- SoGo — 多人协同管理软件
- netdate — 邮件服务器健康监控系统
- iRedAdmin — 邮件服务器管理面板
- Fail2ban — 密码锁

![image-20240806223353413](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806223353413.png)

允许安装清单



![image-20240806223406651](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806223406651.png)

重启服务器，应用配置。

# 4. 启用服务

## 4.1 开放端口

iRedMail邮件服务器在部署时需要开放一些特定的端口以确保邮件服务的正常运行。根据搜索结果，以下是一些需要开放的端口及其用途：

1. 要使用 `ufw` 命令行工具开放上述端口，你可以按照以下步骤操作：

   1. **开放 SMTP 服务端口 25**（用于发送邮件）：
      ```bash
      sudo ufw allow 25/tcp
      ```

   2. **开放 POP3 服务端口 110**（用于接收邮件）：
      ```bash
      sudo ufw allow 110/tcp
      ```

   3. **开放加密的 POP3 服务端口 995**：
      ```bash
      sudo ufw allow 995/tcp
      ```

   4. **开放 IMAP 服务端口 143**（用于接收邮件）：
      ```bash
      sudo ufw allow 143/tcp
      ```

   5. **开放加密的 IMAP 服务端口 993**：
      
      ```bash
      sudo ufw allow 993/tcp
      ```
      
   6. **开放提交邮件服务端口 587**（用于通过 SMTP 发送邮件时使用 TLS 加密）：
      ```bash
      sudo ufw allow 587/tcp
      ```

   7. **开放使用 SSL 加密的 SMTP 服务端口 465**（SMTPS，尽管已被弃用）：
      ```bash
      sudo ufw allow 465/tcp
      ```

   8. **开放 HTTP 服务端口 80**（用于访问 Webmail 界面）：
      ```bash
      sudo ufw allow 80/tcp
      ```

   9. **开放 HTTPS 服务端口 443**（用于安全访问 Webmail 界面）：
      ```bash
      sudo ufw allow 443/tcp
      ```

   执行上述命令后，`ufw` 将会更新防火墙规则，允许流量通过这些端口。请确保在执行这些命令之前，你已经有足够的权限或者使用 `sudo` 来获取必要的权限。

   如果你想要在开放端口的同时指定特定的 IP 地址或网络，你可以在 `allow` 命令中添加 `from` 参数，例如：

   ```bash
   sudo ufw allow from 192.168.1.100 to any port 25
   ```

   这将只允许来自 IP 地址 `192.168.1.100` 的流量访问端口 25。

   完成端口开放后，使用以下命令来查看当前的 `ufw` 规则状态，确保规则已正确添加：

   ```bash
   sudo ufw status
   ```

   这将列出所有当前的 `ufw` 规则，包括你刚刚添加的规则。

使用如 `stunnel` 这样的第三方代理软件来转发端口。这种方法不会更改 MySQL 的默认端口，而是通过代理来转发流量。

1. 安装 `stunnel`：

   ```
   sudo apt-get install stunnel4 # Debian/Ubuntu
   sudo yum install stunnel # CentOS/RHEL
   ```

2. 配置 `stunnel`。创建或编辑配置文件 `/etc/stunnel/stunnel.conf`，添加以下内容：

   ```
   [mysql-port-forward]
   accept = 13306
   connect = 127.0.0.1:3306
   ```

3. 启动 `stunnel` 服务并确保它在系统启动时自动启动：

   ```
   bashsudo systemctl start stunnel4
   sudo systemctl enable stunnel4
   ```

4. 确保防火墙允许从外部访问端口 13306。

## 4.2 启用SSL证书

配合Let's Encrypt与Cloudflare进行托管
需要准备

```
1. Cloudflare账户邮箱
1. Cloudflare API Key `My Profile → API Tokens → Global API Key` 
```

 申请证书的流程

```latex
curl https://get.acme.sh | sh -s email=xxx@mail.com  #请将xxx@mail.com更改为你自用邮箱
```

设置环境变量

```
domain="mx.example.com"  #你的域名邮箱
cf_email="Cloudflare Email"  #请更改为你的Cloudflare Email
cf_key="Cloudflare API Key"  #请更改为你的Cloudflare API Key

# 为域名颁发证书
export CF_Key="${cf_key}"
export CF_Email="${cf_email}"
```

颁发证书

```
~/.acme.sh/acme.sh --issue --dns dns_cf -d "${domain}"
```

安装证书
需要注意的是，这里的iRedMail.key与crt需要确定路径，如果找不到路径就强制安装会导致域名反复重定向。
建议使用find命令找到确切路径

```
~/.acme.sh/acme.sh --install-cert -d "${domain}" --key-file /etc/ssl/private/iRedMail.key --fullchain-file /etc/ssl/certs/iRedMail.crt
```

 重启三项服务

```
service postfix reload
service dovecot reload
service nginx reload
```

禁用灰名单功能

```shell
vim /opt/iredapd/settings.py
```

将

```shell
plugins = ["reject_null_sender", "wblist_rdns", "reject_sender_login_mismatch", "greylisting", "throttle", "amavisd_wblist", "sql_alias_access_policy", "sql_ml_access_policy"]
```

中的 `greylisting` 删除
然后，重启 iredapd

```shell
service iredapd restart
```

# 5. 配置DNS解析

## 5.1 设置PTR反向解析

设置**PTR**需要**联系服务器供应商**，在服务器后台操作
如果后台没有操作，可以向供应商提工单
**说明要添加PTR反向解析到你的邮箱域名**
比如：添加PTR解析到 mx.example.com
检验命令： `nslookup 104.5.6.7` nslookup <你的IP>
不设置PTR会导致邮件被gmail等邮箱服务器拦截。

> 为什么需要反向解析？
> PTR解析和rDNS都是与DNS (Domain Name System,域名系统)相关的概念,下面我来为你详细解释:
>
> 1. PTR解析:
>
> PTR (Pointer Record)是DNS的一种资源记录类型,用于将IP地址映射到域名。它执行从IP地址到域名的反向DNS查找。
> 例如,如果一个IP地址为192.0.2.1,对应的PTR记录可能是 1.2.0.192.in-addr.arpa,指向域名 example.com。
> PTR记录的格式为:
> (IP地址反序).(in-addr.arpa/ip6.arpa) TTL IN PTR 域名。
>
> 1. rDNS (Reverse DNS):
>
> rDNS即反向DNS,是通过IP地址查询域名的过程。它利用PTR记录完成从IP地址到域名的反向解析。
> 正向DNS (Forward DNS)是通过域名查询IP地址,而反向DNS则相反,通过IP地址查询对应的域名。
>
> 1. 用途:
>
> - 反垃圾邮件:许多反垃圾邮件系统使用rDNS来验证发件人IP地址的真实性和可信度,没有有效rDNS记录的IP更可能被识别为垃圾邮件来源。
> - 日志和统计:网络服务日志通常记录客户端IP,使用rDNS可以将IP转换为域名,便于分析和统计访问来源。
> - 身份验证:一些服务(如SSH)可以配置仅允许来自特定主机名的连接,通过rDNS验证客户端IP是否匹配。
> - 信誉评估:搜索引擎等通过rDNS评估一个IP地址的可信度和声誉,影响其抓取频率和排名。
>
> 1. 需要原因:
>
> - 可读性:IP地址难以记忆和识别,而域名更友好、更易读,rDNS提供IP到域名的转换。
> - 安全性:rDNS在身份验证、垃圾邮件识别等方面提供了一定的安全机制。
> - 可管理性:使用域名(通过rDNS转换)而非IP管理服务器,更灵活方便,不受IP变化影响。
> - 合规性:一些标准协议(如SMTP)要求服务器提供有效的rDNS记录。

## 5.2 设置MX三级域名的A记录

![image-20240806230451781](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806230451781.png)

## 5.3 设置MX记录

MX 记录就是邮件的解析记录，非常重要的一条记录，配置根域名的 MX 记录为自己的邮件域名地址，优先级为 10

![image-20240806230622132](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806230622132.png)

## 5.4 设置SPF记录

SPF 记录是为了防止垃圾邮件而设定的，告知收件方，从设置的允许列表中发出的邮件都是合法的，设置方式为添加一条根域名的 TXT 解析记录
内容为 `v=spf1 mx ~all`

![image-20240806230718492](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806230718492-17229568390071.png)

## 5.5 设置DKIM记录

DKIM 可说是避免被判定为垃圾邮件的一大利器，DKIM 属于一种类似加密签名的解析记录，只有包含此加密数据，且公钥与密钥相匹配才属于合法邮件，要设置 DKIM 记录，首先要查询 DKIM 信息。
查询DKIM 信息有两种方式：
**第一种：**在系统中执行命令查看：`amavisd showkeys`
若是出现报错：`Config file "/etc/amavisd.conf" does not exist, at /usr/sbin/amavisd line`
修改 `/usr/sbin/amavisd` 文件
搜索 `config_files = ( '`
把括号里面的路径改为 `‘/etc/amavisd/amavisd.conf’`

**第二种：**直接查看 `/root/iRedMail-1.7.1/iRedMail.tips` 文件，里面有相应的 DKIM
将括号内的文本 _**去除引号以及空格并相连**_ 就是 DKIM 数据
在解析中添加一条 `dkim._domainkey` 的 TXT 解析，内容就是咱们组合出的文本

![image-20240806230825556](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806230825556.png)



![image-20240806231028951](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806231028951-17229570295713.png)

## 5.6 设置DMARC记录

DMARC 记录是当收件方检测到伪造邮件等行为时，将根据您的配置进行操作的一个记录，比如拒绝邮件或放入垃圾邮件以及不做处理等，同时会反馈一份检测报告到配置的邮箱地址内。
添加方法就是增加一条 `_dmarc` 的 TXT 解析，内容为配置选项，

```
v=DMARC1; p=none; pct=100; rua=mailto:dmarc@``example.com
```

注意最后面的`example.com` 需要改成你的域

![image-20240806231132735](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806231132735.png)

# 6. 测试

## 6.1 mail

![image-20240806231527561](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806231527561.png)

## 6.2 iredmail

![image-20240806231520630](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806231520630.png)

## 6.3 SOGo

![image-20240806231733234](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806231733234.png)

## 6.4 netdata

![image-20240806231740266](../assets/img/2024-08-06-dev-Linux%E8%BF%90%E7%BB%B4-IMAP%E9%82%AE%E5%B1%80%E6%96%B9%E6%A1%88/image-20240806231740266.png)
