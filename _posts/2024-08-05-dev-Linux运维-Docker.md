---
layout: post
title: Linux运维-Docker
categories: [Blog, Devops]
tags: [project,web]
date: 2024-08-05 22:54 +0800
---
> AUTOGEN 6cc7fbb9e526427481e86219b6a2279b

# Linux Docker

Docker 是一种开源的应用容器引擎，它允许开发者将应用及其依赖环境打包到一个轻量级、可移植的容器中，然后在任何流行的 Linux 机器上运行，实现虚拟化。Docker 容器作为轻量级的虚拟化技术，与虚拟机相比，具有以下优势：

1. **轻量化**：Docker 容器共享主机操作系统内核，启动迅速，占用资源少 。
2. **标准开放**：基于开放式标准，可在多种基础设施上运行 。
3. **安全隔离**：提供应用的隔离性，问题容器不会影响到整个系统 。

Docker 的主要组成要素包括：
- **镜像**：提供容器运行所需的程序、库、资源和配置参数，是不可变的模板 。
- **容器**：镜像的运行实例，提供隔离化的用户空间 。
- **镜像仓库**：集中存放镜像文件，方便镜像的存储和分发 。

Docker 的工作流程基于客户端/服务器架构，Docker 守护进程作为服务器端接收客户端的请求，负责创建、运行和分发容器 。

Docker 的优点包括快速交付应用程序、响应式部署和扩展、以及在同一硬件上运行更多工作负载 。此外，Docker 提供了一致的运行环境，有助于解决开发过程中的环境一致性问题，并支持持续集成和持续部署 。

与传统虚拟机相比，Docker 容器具有更高效的资源利用、更快的启动时间，并且能够提供一致的运行环境，简化了应用的迁移、维护和扩展 。简而言之，Docker 是一种容器化技术，通过封装应用及其运行环境，实现了应用的快速、一致和灵活部署 。

## 1. 社区版和企业版

Docker 社区版（CE）和企业版（EE）是Docker公司的两种不同版本，它们在功能和定位上有所区别：

1. **Docker CE**：是免费的、开源的版本，适合个人开发者和小团队使用。它提供了Docker的基础功能，包括容器引擎、镜像管理等，但可能缺少一些高级特性和企业级支持。

2. **Docker EE**：是面向企业的商业版本，提供了额外的功能和企业级支持。企业版包括了社区版所有功能，并增加了一些高级功能，如：
   - 混合操作系统集群支持，允许在Linux和Windows Server上运行和管理容器。
   - 增强的基于角色的访问控制（RBAC），提供了更细致的权限管理。
   - 自动镜像升级和不可变的存储库，确保镜像的完整性和安全性。
   - Docker安全扫描，支持对Linux和Windows镜像进行安全漏洞扫描。

Docker EE还分为三个不同的订阅级别：基础版、标准版和高级版，每个版本提供不同级别的服务和支持。例如，基础版提供认证的基础设施和支持，而高级版则包括安全扫描和安全漏洞监控等高级功能。

企业版还提供了更全面的集成容器管理、安全性和支持，适合在大规模生产环境中构建、运送和运行关键业务应用程序。此外，企业版还提供了更长时间的支持周期，而社区版通常只提供6个月的支持。

总的来说，Docker CE适合那些希望免费使用Docker并尝试基于容器的应用程序部署的小企业和IT团队。而Docker EE则为需要在生产环境中大规模部署和管理容器化应用程序的企业提供了更强大的功能和支持。

## 2. 快速安装

1. 安装依赖

   ```
   yum install -y yum-utils device-mapper-persistent-data lvm2
   ```

2. 安装阿里云镜像源

   ```
   yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
   ```

3. 安装社区版

   ```
   yum install -y docker-ce
   ```

4. 启用Docker（开机自启）

   ```
   #启动docker命令
   systemctl start docker
   #设置开机自启命令
   systemctl enable docker
   #查看docker版本命令
   docker version
   ```

# 稳定版安装

安装18.3稳定版的介绍

## 安装18.03

```bash
yum update
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install docker-ce-18.03.1.ce
```

安装最新版

```bash
yum install docker-ce -y
```

## 更新源

在Docker Image镜像源无法使用后，可以通过使用阿里云提供的镜像加速服务为自己的镜像提供加速

```json
https://vhfa9jwg.mirror.aliyuncs.com
```

linux部署

```latex
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://vhfa9jwg.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 重启Docker服务

```bash
systemctl restart docker
```

## 构建Docker镜像

```bash
docker build --tag NAME .
```

## 运行Docker

```bash
docker run -p 80:80 -d TAGNAME
```

# 基本介绍

## Docker概念

1. 镜像：用于创建容器的模板，类似于class
2. 容器：一个实际运行的实体，是镜像实例化出来的对象
3. 客户端：与docker守护进程通信，例如命令行
4. 主机：运行守护进程和其它容器的物理机
5. Registry docker的镜像仓库。一个仓库包含了一个软件不同版本的镜像，<仓库名>：<标签>
6. docker machine: 简化的dockers命令行工具

## Dockers安装

阿里云自动安装

```bash
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

手动shell安装

```bash
 curl -fsSL https://get.docker.com -o get-docker.sh $ sudo sh get-docker.sh
```

如果要使用 Docker 作为非 root 用户，则应考虑使用类似以下方式将用户添加到 docker 组：

```bash
sudo usermod -aG docker your-user
```

## CentOS 7安装

```bash
yum update
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum install docker-ce-18.03.1.ce


# OR install latest
yum install docker-ce -y
```

## 卸载 docker

删除安装包：

```bash
sudo apt-get purge docker-ce
```

删除镜像、容器、配置文件等内容：

```bash
sudo rm -rf /var/lib/docker
```

脚本安装进行用户管理的操作

```bash
sudo groupadd docker     #添加docker用户组
sudo gpasswd -a $USER docker     #将登陆用户加入到docker用户组中
newgrp docker     #更新用户组
sudo systemctl restart docker   # 重启docker
docker ps    #测试docker命令是否可以使用sudo正常使用

```

## Docker更新镜像源

更改/etc/docker/daemon.json文件

```json
# 创建或修改 /etc/docker/daemon.json 文件，修改为如下形式
{
    "registry-mirrors" : [
    "https://registry.docker-cn.com",
    "https://docker.mirrors.ustc.edu.cn",
    "http://hub-mirror.c.163.com",
    "https://cr.console.aliyun.com/"
  ]
}
# 重启docker服务使配置生效
$ systemctl restart docker.service

```

在Docker Image镜像源无法使用后，可以通过使用阿里云提供的镜像加速服务为自己的镜像提供加速

```json
https://vhfa9jwg.mirror.aliyuncs.com
```

linux部署

```latex
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://vhfa9jwg.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 常用命令

### 查询本地安装的镜像

```bash
docker image ls
```

### docker安装一个ubuntu镜像

查找Ubuntu镜像

```bash
docker search ubuntu
```

安装Ubuntu镜像

```bash
docker pull ubuntu
```

运行helloworld

```bash
docker run ubunut /bin/echo "hello world"
```

### 交互式的容器

本质上是创建一个伪终端并且允许STDIN进行交互。

```bash
docker run -i -t ubuntu /bin/bash
```

-i 参数允许新建一个终端
-t 允许进行交互

### 启动后台模式

```bash
docker run -d ubuntu /bin/sh -c "while true;do echo hello world; sleep 1;done"
```

-d后台运行

### 列出正在运行的docker

docker ps
ps中的七种状态

- created（已创建）
- restarting（重启中）
- running 或 Up（运行中）
- removing（迁移中）
- paused（暂停）
- exited（停止）
- dead（死亡）

### 查看运行的日志

```bash
docker logs ID
```

### 停止容器

```bash
docker stop ID
```

### 进入容器

```bash
docker attach  # 导致容器停止
docker exec  # 容器不停止
```

进入一个ITD容器

```bash
docker exec -it ID /bin/bash
```

### 导出容器

导出当前容器的快照

```bash
docker export id > ubuntu.tar
```

导出后导入

```bash
cat docker/ubuntu.tar | docker import - test/ubuntu:v1
```

也可以从某个连接导入

```bash
docker import URL
```

### 删除容器

```bash
docker rm -f ID
```

### 启动一个web应用

首先在启动一个应用

```bash
docker run train/webapp # 载入镜像
docker run -d -P train/webapp python app.py
```

### 映射不同端口

```bash
docker run -d -p 源端口:新端口 train/webapp python app.py
```

### 查看不同端口

```bash
docker port ID
```

### 查看webapp的输出日志

这里的 日志是输出到控制台的日志

```bash
docker logs -f ID
```

### 查看容器内部的进程

```bash
docker top ID
```

### 查看webapp的底层信息

```bash
docker inspect ID
```

## docker镜像

### 镜像列表

```bash
docker images
docker image ls
```

- **REPOSITORY：**表示镜像的仓库源
- **TAG：**镜像的标签
- **IMAGE ID：**镜像ID
- **CREATED：**镜像创建时间
- **SIZE：**镜像大小

### 下载新的镜像源

```bash
docker pull <id>:version
```

### 查找镜像

```bash
docker search ?
```

### 快速删除镜像

```bash
docker rmi <image name>
```

## 构建镜像Dockerfile

使用构建命令来构建一个新镜像

```bash
FROM    centos:6.7 # 来自的镜像源
MAINTAINER      Fisher "fisher@sudops.com"  # 维护者

RUN     /bin/echo 'root:123456' |chpasswd  # 运行的命令
RUN     useradd runoob
RUN     /bin/echo 'runoob:123456' |chpasswd
RUN     /bin/echo -e "LANG=\"en_US.UTF-8\"" >/etc/default/local
EXPOSE  22  # 向外开放的端口
EXPOSE  80  # 向外开放的端口
CMD     /usr/sbin/sshd -D  # 运行的命令
```

### 示例

一个fastapi项目
Dockerfile

```dockerfile
# Use the official Python image as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the app's dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install uvicorn python-multipart

# Copy the rest of the app's code into the container
COPY . .

# Expose the port that the app will run on
EXPOSE 80

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
```

构建

```bash
docker build --tag file_server_api .
```

名字务必为lowercase
运行

```bash
 docker run -p 80:80 -d file_server_api
```

# 网络

在Docker中管理网络是实现容器间通信和隔离的关键部分。以下是一些基本的网络管理概念和命令：

1. **默认桥接网络**：
   - 当你创建一个Docker容器时，如果没有指定网络，Docker会默认创建一个桥接网络（bridge network），并给容器分配一个私有的IP地址。
2. **查看网络**：
   - 使用 `docker network ls` 来列出所有Docker网络。
3. **查看网络详情**：
   - 使用 `docker network inspect <network_name>` 来获取特定网络的详细信息。
4. **创建网络**：
   - 使用 `docker network create` 来创建一个新的网络。你可以指定网络的类型，如桥接（bridge）、覆盖（overlay）或主机（host）等。
5. **连接容器到网络**：
   - 在创建容器时，使用 `docker run --network=<network_name>` 将容器连接到指定的网络。
6. **断开容器与网络**：
   - 使用 `docker network disconnect <network_name> <container_name>` 将容器从网络中断开。
7. **删除网络**：
   - 使用 `docker network rm <network_name>` 来删除一个网络。只有当网络中没有容器时，才能删除该网络。
8. **使用自定义网络**：
   - 你可以创建自定义网络来实现容器间的通信，或者将容器连接到外部网络。
9. **覆盖网络**：
   - 对于跨主机或跨云服务的容器通信，可以使用覆盖网络（overlay network）。这通常用于Docker Swarm模式。
10. **主机网络**：
    - 使用 `docker run --network=host` 将容器直接连接到宿主机的网络，共享宿主机的IP地址和端口。
11. **端口映射**：
    - 使用 `-p` 或 `--publish` 选项在 `docker run` 命令中将容器端口映射到宿主机端口，实现外部访问。
12. **网络别名**：
    - 在连接容器到网络时，可以使用 `--alias` 选项为容器设置别名，以便在容器间通信时使用。
13. **网络安全**：
    - 可以使用网络安全策略来限制容器间的通信，例如只允许特定容器之间进行通信。
14. **网络插件**：
    - Docker支持第三方网络插件，如Weave, Calico等，提供更高级的网络功能。

通过这些命令和概念，你可以有效地管理Docker容器的网络，实现容器之间的隔离和通信。

# Docker Compose

Docker Compose是一个用于定义和运行多容器Docker应用程序的工具。通过Compose，你可以使用YAML文件来配置你的应用服务，然后使用一个单一的命令来创建和启动所有服务。

### 安装Docker Compose

1. **通过官方安装脚本**（推荐方式）：
   - 在Linux系统上，你可以使用官方提供的安装脚本。首先，下载并运行安装脚本：
     ```bash
     curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
     ```
   - 然后，更改二进制文件的权限，使其可执行：
     ```bash
     chmod +x /usr/local/bin/docker-compose
     ```

2. **手动下载**：
   - 你可以从[Docker Compose的GitHub发布页面](https://github.com/docker/compose/releases)手动下载适用于你的操作系统和架构的版本。

3. **通过包管理器**：
   - 对于某些操作系统，Docker Compose可能可用在你的包管理器中。例如，在Debian或Ubuntu上，你可以使用：
     ```bash
     sudo apt-get install docker-compose
     ```

4. **使用pip**（Python用户）：
   - Docker Compose也可以通过Python的包管理器pip安装：
     ```bash
     pip install docker-compose
     ```
   - 这种方式安装的Compose可能不在系统的PATH中，你可能需要手动将其添加到PATH。

### 使用Docker Compose

1. **创建`docker-compose.yml`文件**：
   - 在你的项目目录中，创建一个`docker-compose.yml`文件，定义你的服务、网络和卷。以下是一个基本的示例：
     ```yaml
     version: '3'
     services:
       web:
         image: nginx:alpine
         ports:
           - "8080:80"
       db:
         image: postgres
         environment:
           POSTGRES_DB: dbname
           POSTGRES_USER: user
           POSTGRES_PASSWORD: password
     ```

2. **启动服务**：
   - 在项目目录中，运行以下命令来启动所有服务：
     ```bash
     docker-compose up -d
     ```
   - `-d` 参数表示在后台运行。

3. **查看服务状态**：
   - 使用以下命令查看所有服务的状态：
     ```bash
     docker-compose ps
     ```

4. **停止服务**：
   - 要停止所有服务，使用：
     ```bash
     docker-compose down
     ```

5. **查看日志**：
   - 查看服务的日志，例如web服务的日志：
     ```bash
     docker-compose logs web
     ```

6. **执行命令**：
   - 在服务容器内执行命令，例如进入web服务的bash：
     ```bash
     docker-compose exec web sh
     ```

7. **构建服务**：
   - 如果你的`docker-compose.yml`文件中使用了`build`选项，你可以使用以下命令来构建服务：
     ```bash
     docker-compose build
     ```

8. **扩展服务**：
   - 使用`docker-compose up --scale`命令可以扩展服务的副本数量，例如扩展web服务为3个副本：
     ```bash
     docker-compose up --scale web=3 -d
     ```

Docker Compose提供了一种快速、简洁的方式来管理多容器Docker应用程序，非常适合开发、测试和生产环境。
