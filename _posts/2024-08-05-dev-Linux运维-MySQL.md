---
layout: post
title: Linux运维-MySQL
categories: [Blog, Devops]
tags: [web]
date: 2024-08-05 23:03 +0800
---
> AUTOGEN fc6be5936a5a43939e705475c4e2ccda

# Linux MySQL

## 介绍

MySQL是一个广泛使用的开源关系数据库管理系统（RDBMS），它基于结构化查询语言（SQL）进行操作。MySQL由瑞典的MySQL AB公司开发，后来被Sun Microsystems收购，最终成为了Oracle公司的一部分。它以其性能、可靠性和易用性而闻名，被广泛应用于各种应用程序，包括网站、企业应用和数据仓库。

### MySQL 5.7 和 8.0 的关系

MySQL 5.7 和 MySQL 8.0 都是MySQL数据库的版本，它们之间存在一些关键的差异和改进：

1. **性能改进**：MySQL 8.0 在性能方面进行了优化，包括更快的查询执行和更好的索引性能。
2. **默认字符集**：MySQL 8.0 将默认字符集从`latin1`更改为`utf8mb4`，这支持更多的Unicode字符，包括表情符号。
3. **窗口函数**：MySQL 8.0 引入了窗口函数，这使得在SQL查询中可以更容易地执行复杂的分析和聚合操作。
4. **JSON 支持**：MySQL 8.0 增强了对JSON数据类型的支持，包括更多的JSON函数和操作。
5. **数据字典**：MySQL 8.0 引入了一个新的系统数据库`mysql_innodb_cluster_metadata`，用于存储InnoDB集群的元数据。
6. **安全性**：MySQL 8.0 引入了更多的安全特性，包括密码过期策略和角色支持。
7. **去除了某些特性**：MySQL 8.0 去除了某些在早期版本中的特性，例如`LOAD DATA INFILE`的`LOCAL`关键字。

### MySQL 的基本使用方法

以下是使用MySQL的一些基本步骤：

1. **安装MySQL**：首先，你需要在你的系统上安装MySQL。可以从[MySQL官网](https://dev.mysql.com/downloads/)下载适合你操作系统的版本。

2. **启动MySQL服务**：安装完成后，需要启动MySQL服务。这通常可以通过系统的服务管理工具来完成。

3. **连接到MySQL**：使用MySQL客户端工具（如命令行客户端）连接到MySQL服务器。可以通过以下命令连接：
   ```bash
   mysql -u username -p
   ```
   其中`username`是你的数据库用户名，`-p`会提示你输入密码。

4. **创建数据库**：连接到MySQL后，你可以创建一个新的数据库：
   ```sql
   CREATE DATABASE mydatabase;
   ```

5. **选择数据库**：创建数据库后，选择它以便进行操作：
   ```sql
   USE mydatabase;
   ```

6. **创建表**：在数据库中创建表以存储数据：
   ```sql
   CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       username VARCHAR(50) NOT NULL,
       password VARCHAR(50) NOT NULL
   );
   ```

7. **插入数据**：向表中插入数据：
   ```sql
   INSERT INTO users (username, password) VALUES ('user1', 'pass1');
   ```

8. **查询数据**：使用SELECT语句查询数据：
   ```sql
   SELECT * FROM users;
   ```

9. **更新数据**：使用UPDATE语句更新数据：
   ```sql
   UPDATE users SET password = 'newpass1' WHERE username = 'user1';
   ```

10. **删除数据**：使用DELETE语句删除数据：
    ```sql
    DELETE FROM users WHERE username = 'user1';
    ```

11. **退出MySQL**：完成操作后，可以通过以下命令退出MySQL：
    ```sql
    EXIT;
    ```

这些是使用MySQL的基本步骤。MySQL提供了丰富的功能和强大的SQL语句，可以满足各种数据存储和管理的需求。

# 本地安装

## 5.7 

## 8.0 

# Docker安装

在Docker上安装MySQL是一个相对简单的过程，以下是基本步骤：

1. **搜索并拉取MySQL镜像**：你可以在Docker Hub上搜索MySQL的官方镜像，然后使用`docker pull`命令来拉取所需的MySQL版本镜像。例如，对于MySQL 5.7，你可以使用命令`docker pull mysql:5.7`来拉取镜像。

2. **创建并运行容器**：使用`docker run`命令来创建并启动一个新的容器实例。你可以通过`-p`参数将容器的端口映射到宿主机的端口，使用`-e`参数设置环境变量，比如MySQL的初始密码，使用`--name`参数为容器指定一个名称，使用`-d`参数让容器在后台运行。例如：
   ```bash
   docker run -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.7
   ```
   这将启动一个名为`mysql`的容器，设置root用户的密码为`123456`，并将容器的3306端口映射到宿主机的3306端口。

3. **配置持久化存储**：为了确保MySQL数据的持久化，你可以使用`-v`参数将宿主机的目录挂载到容器内部。例如：
   ```bash
   -v $PWD/data:/var/lib/mysql
   ```
   这将把当前宿主机目录下的`data`目录挂载到容器的MySQL数据目录`/var/lib/mysql`。

4. **配置MySQL**：如果需要自定义MySQL的配置，你可以将宿主机上的`my.cnf`配置文件挂载到容器的`/etc/mysql/my.cnf`路径下。例如：
   ```bash
   -v $PWD/conf/my.cnf:/etc/mysql/my.cnf
   ```
   这样，容器启动时就会使用自定义的配置文件。

5. **连接MySQL**：容器启动后，你可以使用`docker exec`命令进入容器内部，然后使用MySQL客户端连接到数据库。例如：
   ```bash
   docker exec -it mysql /bin/bash
   mysql -uroot -p
   ```
   输入设置的root密码即可登录MySQL。

6. **安全设置**：出于安全考虑，你可能需要运行`mysql_secure_installation`脚本来增强MySQL的安全性，设置root密码、删除匿名用户、禁止root用户远程登录等。

7. **注意事项**：对于MySQL 8.0.15及更早版本，你可能需要在MySQL Server容器中运行`mysql_upgrade`实用程序来完成升级过程，这在MySQL 8.0.16及更高版本中不再需要。

以上步骤提供了在Docker上安装MySQL的基本流程，具体操作可能会根据你的具体需求和服务器环境有所不同。
