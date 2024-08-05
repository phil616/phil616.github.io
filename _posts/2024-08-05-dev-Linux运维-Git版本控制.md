---
layout: post
title: Linux运维-Git版本控制
categories: [Blog, Devops]
tags: [web]
date: 2024-08-05 23:32 +0800
---
> AUTOGEN 093d3878bef04b3b9b0d9d2d887e7eaf
# Linxu Git

# 1 快速开始

> 通过寻找下面的四个步骤可以快速开始上手一个合作项目

1. 配置用户名
2. 配置身份认证
3. Git基本工作流
4. Git推送与协作

# 2 详细描述

## 2.1 简介

Git 是用于 [Linux内核](https://baike.baidu.com/item/Linux%E5%86%85%E6%A0%B8/10142820)开发的[版本控制](https://baike.baidu.com/item/%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6)工具。与常用的版本控制工具 CVS, Subversion 等不同，它采用了分布式版本库的方式，不必服务器端软件支持，使源代码的发布和交流极其方便。 Git 的速度很快，这对于诸如 Linux kernel 这样的大项目来说自然很重要。 Git 最为出色的是它的合并跟踪（merge tracing）能力。
实际上内核开发团队决定开始开发和使用 Git 来作为内核开发的版本控制系统的时候，世界开源社群的反对声音不少，最大的理由是 Git 太艰涩难懂，从 Git 的内部工作机制来说，的确是这样。但是随着开发的深入，Git 的正常使用都由一些友好的脚本命令来执行，使 Git 变得非常好用，即使是用来管理我们自己的开发项目，Git 都是一个友好，有力的工具。现在，越来越多的著名项目采用 Git 来管理项目开发.
Git和SVN最主要的区别：SVN是集中式版本控制系统，Git是分布式版本控制系统，SVN拥有中央服务器，必须联网，Git是分布式的，没有中央服务器，Git可以直接看到更新了那些代码和文件。

## 2.2 Git下载

官网：[https://git-scm.com/](https://git-scm.com/)
镜像下载
[https://npm.taobao.org/mirrors/git-for-windows/](https://npm.taobao.org/mirrors/git-for-windows/)
在下载其他的安装包时，都可使用镜像下载
[https://developer.aliyun.com/mirror/NPM?from=tnpm](https://developer.aliyun.com/mirror/NPM?from=tnpm)

## 2.3 工作原理

Git本地有三个工作区域：工作目录（Working Directory）、暂存区(Stage/Index)、资源库(Repository或Git Directory)。如果在加上远程的git仓库(Remote Directory)就可以分为四个工作区域。
![image-20240805233513034](../assets/img/2024-08-05-dev-Linux%E8%BF%90%E7%BB%B4-Git%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6/image-20240805233513034.png)
git 工作流如下：

1. 在工作目录中添加、修改文件；
2. 将需要进行版本管理的文件放入暂存区域；
3. 将暂存区域的文件提交到git仓库。

因此，git管理的文件有三种状态：已修改（modified）,已暂存（staged）,已提交(committed)

## 2.4 配置

所有的配置文件都保存在了本地
快速查看配置`git config -l`
查看不同级别的配置文件：

```bash
#查看系统
git config --system --list　　
#查看当前用户（global）配置git 
config --global --list
```

系统级别配置 (system)：适用于系统上所有用户和所有仓库，通常存储在 /etc/gitconfig 文件中（路径可能因操作系统不同而有所变化）。
用户级别配置 (global)：适用于特定用户的所有仓库，存储在用户主目录下的 .gitconfig （或 _gitconfig，具体取决于操作系统）文件中。
仓库级别配置 (local)：适用于特定仓库的配置，存储在该仓库的 .git 目录中的 config 文件中。
查看基本配置

```bash
git config
git config --list
```

针对当前仓库单独配置

```bash
git config -e
```

该命令会使用文本编辑器打开当前仓库的配置文件
如果修改全局配置文件

```bash
git config -e --global
```

别名到命令的映射
当常用命令较长时，可以使用bashrc命令来使用别名代替长命令。

1. 打卡~目录、或用户目录
2. 创建`.bashrc`文件

```bash
touch ~/.bashrc
```

3. 使用常用命令

```bash
# 用于输出git提交日志
alias git-log='git log --pretty=oneline --all --graph --abbrev-commit'
#用于输出当前目录所有文件及基本信息
alias ll='ls -al'
```

4. 使bash文件生效

```bash
source ~/.bashrc
```

查看全局配置文件

```bash
git config --global -e
```

解决平台回车问题
在windows下，应该将autocrlf设为true

```bash
git config --global core.autocrlf true
```

在macOS环境下，应该设为input

```bash
git config --global core.autocrlf input
```

使用VSCode

```bash
git config --global core.editor "code --wait"
```

使用notepad

```bash
git config --global core.editor "notepad --wait"
```

windows系统在git安装时，会在安装程序的安装步骤设置一个默认的编辑器
推荐使用VSCode和notepad++两款编辑器。

## 2.5 配置用户

当你安装Git后首先要做的事情是设置你的用户名称和e-mail地址。这是非常重要的，因为每次Git提交都会使用该信息。它被永远的嵌入到了你的提交中：

```bash
git config --global user.name "kuangshen"  #名称
git config --global user.email "24736743@qq.com"   #邮箱
```

只需要做一次这个设置，如果你传递了--global 选项，因为Git将总是会使用该信息来处理你在系统中所做的一切操作。如果你希望在一个特定的项目中使用不同的名称或e-mail地址，你可以在该项目中运行该命令而不要--global选项。总之--global为全局配置，不加为某个项目的特定配置。

# 3 常用命令

暂存区 -> 本地仓库
使用提交命令将暂存区的文件存储到本地仓库

```bash
git commit
```

git commit 命令可以添加注解，后接-m来添加注释

```bash
git commit -m "this is first commit"
```

## 3.3 工作区的状态

1. 查看当前仓库所有变更文件的状态

```bash
git status
```

2. 比较在暂存区和工作区的不同文件

```bash
git diff
```

3. 在暂存区和工作区之间切换

```bash
# 工作区放到暂存区
git add <file>
# 暂存区到工作区
git rm --cached <file>
```

4. 修改的情况

被提交的文件如果被修改，则git diff 中会有修改情况，
需要先添加到工作区，再提交到仓库

```bash
git add <file>
git commit
# 或者将以上二者结合
git commit -a
```

提交的状态
提交的状态由五个部分组成

1. 当前的提交id
2. 提交的注释信息
3. 提交的时间
4. 提交的作者
5. 提交时的完整代码快照

文件的状态切换
新建的文件不会在暂存区中，会被存储在工作区中，此时使用 git status 命令，会显示出红色端点未跟踪“untracked”文件。
使用git add 添加后，将文件添加到暂存区（staged）。
当文件被更改时，status仍然会显示红色字体，但是提示的信息会从“未跟踪”变为“更改未暂存”（chang）
对于文件而言，存在如下情况：
文件被创建 -> untracked
文件被添加到暂存区 -> staged 、 to be commited
暂存区文件被修改 -> unstaged
文件再次被添加 -> staged
提交当前暂存区 -> commited
暂存区文件被更改 -> unstaged 从仓库直接转为工作区

## 3.4 查看日志

### 基本log

```bash
git log
```

git log是查看简短日志的方式，同时git log支持多种变形的方式查看日志

1. --all 查看所有分支
2. --pretty=oneline 提示信息显示为一行
3. --abbrev-commit 缩短commitid信息
4. --graph以图形化界面显示日志信息

注意事项
当提交记录的历史很长时，日志会通过vim显示，需要了解vim的使用方式（j向下显示，k向上显示）
各个命令可用组合使用
例如常见的速览方式为：

```bash
git log --all --abbrev-commit --pretty=oneline --graph
```

代表着优化commitID长信息，一行显示内容，并且以图形方式显示。
可以将上述的命令命名为别名加入到别名文件中。

### reflog

`git reflog`是参考日志，参考日子可以显示所有可引用的历史版本记录
reflog存储的是操作的记录，而log命令存储的是对于当前的版本记录。如果版本记录发生过回退，则log不应该存储新版本。但回退本身是一种操作，应该被记录在操作日志中。
因此reflog记录的是HEAD的指针变化。
参数说明

- 最前面是历史提交commit-id的前7位，根据这7位可以将版本库恢复到对应节点状态。
- HEAD@{n}：表示HEAD更改历史记录，最新的更改在上面。
- HEAD@{2}：表示HEAD指针在两次移动之前的情况。
- master@{one.week.ago}：表示master分支在本地仓库一周之前的情况。
- 通过HEAD@{n}语法可以回退到指定的提交。例如：git reset --hard HEAD@{3}。
- 与HEAD@{n}与HEAD~n功能类似，但是HEAD~n回退的是git log命令显示的历史提交记录，而HEAD@{n}回退的是git reflog命令显示的历史提交记录。
- 最后一个冒号后面的字串为，该提交的说明信息摘要。

# 4. 分支

## 4.4 解决冲突

当不同分支处理同一个文件时，可能会引发系统无法处理的冲突，例如两个分支处理了同一行代码，则在合并分支的时候，会出现冲突。
此时就需要我们手动处理冲突。
解决冲突的流程

1. 合并分支 `git merge dev`
2. 出现冲突

```latex
$ git merge dev
Auto-merging hello.txt
CONFLICT (content): Merge conflict in hello.txt
Automatic merge failed; fix conflicts and then commit the result.
```

3. 打开出现冲突的文件，也就是hello.txt

```latex
hello 
<<<<<<< HEAD
hello,myworld 
=======
hello,world 
>>>>>>> dev
```

由于我们要确定出问题所在，因此修改hello.txt的内容为合适的内容

4. 修改完成后，`git add .`
5. 提交修改`git commit -m "resolve comflict"`

此时冲突就得到了解决。

## 4.5 常见开发规范

是生产中，各个分支和常用的模型不能随意使用，一般而言，各个分支命名如下：

1. `master`（生产）分支：主要的生产分支，用于正式上线产品的分支
2. `dev/develop`（开发）分支：用于开发的主要分支，开发任务完成后，将此分支合并到master分支
3. `feature`（功能）分支：同期并行的开发分支，用于开发部门各任务组分支，需要合并到开发分支。
4. `hotfix`（修复）分支：master的派生分支，用于线上修复紧急bug，需要合并到其它所有分支
5. `test`（测试）分支：一般是从开发分支派生而来，用于测试部门测试的分支
6. `pre`（预上线）分支：一般是从测试完成的分支派生而来，用于在模拟机上进行实验。

各个开发分支的使用可以组成开发模型，例如下面常见的开发分支的使用：
![image-20240805233530667](../assets/img/2024-08-05-dev-Linux%E8%BF%90%E7%BB%B4-Git%E7%89%88%E6%9C%AC%E6%8E%A7%E5%88%B6/image-20240805233530667.png)

## 4.6 任务分支模型

任务分支模型也称（Feature Branch Workflow）：
每个新功能或修复都会创建一个独立的分支，从main分支切出，开发完成后，通过Pull Request合并回main分支。
每个成员或是功能负责人都负责了一个分支。
具体流程如下：

### 创建和克隆仓库

一个用户创建仓库并上传到GitHub。
其他用户通过git clone <repository-url>克隆这个仓库到他们的本地机器。

### 创建分支

每个用户在开始新功能或修复错误时，从main分支创建一个新的分支，例如git checkout -b feature-branch。

### 开发和提交

在各自的分支上进行开发并提交更改，例如git commit -m "Add new feature"。

### 同步更新

定期将main分支的最新更改合并到自己的分支中，以保持分支同步，例如：bash复制

```
git checkout main
git pull origin main
git checkout feature-branch
git merge main
```

### 创建Pull Request (PR)

功能开发完成后，用户将分支推送到远程仓库，例如git push origin feature-branch。
在GitHub上创建一个Pull Request (PR)，请求将更改合并到main分支。

### 代码审查和讨论

其他团队成员审查PR中的代码，提出反馈意见或建议改进。
作者根据反馈进行必要的修改并更新PR。

### 合并Pull Request

当PR通过审查并且所有测试通过后，管理员或有权限的用户将PR合并到main分支。

### 删除分支

合并之后，删除已合并的分支以保持仓库整洁，例如：bash复制

```
git branch -d feature-branch
git push origin --delete feature-branch
```

### 持续成和部署

配置持续集成（CI）工具，在每次合并到main时自动运行测试和部署。

## 4.7 忽略文件

对于忽略文件而言，每行都对应一个忽略规则，具体语法如下：

1. 反斜杠用于转义\
2. 叹号！用于逻辑取反
3. /标识目录
4. *为任意单个通配符
5. **为任意多个通配符
6. []用于匹配字符列表

常见匹配示例：

```git
bin/: 忽略当前路径下的bin文件夹，该文件夹下的所有内容都会被忽略，不忽略 bin 文件

/bin: 忽略根目录下的bin文件

/*.c: 忽略 cat.c，不忽略 build/cat.c

debug/*.obj: 忽略 debug/io.obj，不忽略 debug/common/io.obj 和 tools/debug/io.obj

**/foo: 忽略/foo, a/foo, a/b/foo等

a/**/b: 忽略a/b, a/x/b, a/x/y/b等

!/bin/run.sh: 不忽略 bin 目录下的 run.sh 文件

*.log: 忽略所有 .log 文件

config.php: 忽略当前路径的 config.php 文件

```

对于后加入的忽略文件而言，忽略文件只能作用于之后的版本，之前的文件如果在忽略文件创建之前就已经生成，则忽略文件不会忽略他们。

### 规则不生效

如果规则不生效，则需要删去本地缓存，将文件改为未跟踪状态，再进行提交。

```git
git rm -r --cached .
git add .
git commit -m 'update .gitignore'
```

### 强制不忽略

你想添加一个文件到Git，但发现添加不了，原因是这个文件被.gitignore忽略了：
可以使用强制添加

```bash
git add -f App.class
```

# 5 远程仓库

本地git每次操作远程仓库时，都需要提供用户名密码， 可以通过配置SSH的方式来让省略身份验证的过程。

1. 生成一个本地的RSA公钥私钥对，`ssh-keygen -t ras`
2. 查看结果文件，一般为` /c/Users/do616/.ssh/id_rsa`和`/c/Users/do616/.ssh/id_rsa.pub`
3. 将公钥上传到远程仓库的SSH配置区域
4. 使用`ssh -T git@github.com`测试，如果提示中出现`You've successfully authenticated`则证明认证完成。

> 为何上传公钥就无需使用密码？
> RSA认证体系通过非对称加密算法和SHA数字签名技术来起到和用户认证相同的保密效果。
> 本地用户向服务器发送信息时，会通过HTTPS加密协议传输，服务器向本地返回信息时，会使用提供的公钥进行加密，而只有本地机拥有私钥能够解密。

## 5.1 远端仓库配置

在远程托管平台完成仓库创建后，需要我们将远程仓库添加到本地

1. 初始化本地仓库的内容，需要本地仓库存在一个commit
2. 通过`git branch -M main`将本地的分支重命名为`main`，git默认的主分支为master，而远程托管平台默认为main。其中`-M`是`--move --force`强制重命名当前分支的缩写
3. `git remote add origin <URL>`来关联远程仓库，远程仓库名称为`origin`。
4. `git push -u origin main`来讲main分支推送到origin，其中`-u`是命令`--set-upstream`的缩写
5. 查看本地分支和远程分支的关联关系`git branch -vv`

## 5.2 远程版本控制规定

1. 明晰注释和提交消息，小型项目可以忽略，但大型项目需要构建严格的消息规范
2. 先提交本地修改，再切换分支
3. 代码及时提交，及时更新
4. 遇到问题不删除文件

---

1.1 创建远程库地址别名

```
git remote -v  #查看远程地址别名
git remote add 别名 远程地址 
例子：git remote add origin https://xx
```

1.2 推送
`开发修改完把本地库的文件推送到远程仓库` `前提是提交到了本地库才可以推送`

```
git push 别名 分支名
git push -u 别名 分支名    #-u指定默认主机
例子：git push origin master
```

1.3 克隆
`完整的把远程库克隆到本地`  `克隆下来后不要在主分支里面做开发` `clone进行一次，从无到有的过程，更新用pull`

```
git clone  远程地址
例子：git clone https://xx
```

1.4 拉取
`本地存在clone下来的文件 就用pull更新`

```
pull = fetch + merge
	git fetch 别名 分支名
	git merge 别名 分支名
git pull 别名 分支名
```

1.5 解决冲突
`注意：解决冲突后的提交是不能带文件名的`
`如果不是基于远程库最新版做的修改不能推送，必须先pull下来安装冲突办法解决`
1.6 rebase
`提交记录简洁不分叉`  `没学懂，感觉有点鸡肋` `混眼熟`

```
git rebase -i 索引号
git rebase -i HEAD~3  #合并最近三条记录
说明：在vim编辑里面改成s
```

1.7 beyond compare
`用软件解决冲突`

```
1.安装 ：
   beyond compare 
2.配置：
   git config --local merge.tool bc3  #合并名称
   git config --local mergetool.path '/usr/local/bin/bcomp' #软件路径
   git config --local mergetool.keepBackup false  #False不用保存备份
3.应用：
   git mergetool
说明：--local指只在当前操作系统有效
```

1.8 跨团队合作
`代码review之后合并`

- **适用于个人**
  **邀请成员**:`Settings` --> `Collaborators` -->`填写用户名` -->`打开链接接受邀请`
- **企业**   `创建一个组织` `方便管理`
- **review**
  `组织做review`  `通过Pull request`
- **给开源社区共享代码**
  `点击别人仓库的fork 到自己的仓库`   -- > `然后clone下来 修改后推送到远程库`  --> `点击Pull Request请求` --> `Create pull request发消息`

1.9 Tag标签
`为了清晰的版本管理，公司一般不会直接使用commit提交`

```
git tag -a v1.0 -m '版本介绍'   #创建本地tag信息
git tag -d v1.0    		#删除tag
git push origin --tags   #将本地tag信息推送到远程库
git pull origin --tags    #拉取到本地

git checkout v.10    #切换tag
git clone -b v0.1 地址   #指定tag下载代码
```

1.10 SSH 免密登录

- 输入:`ssh-keygen -t rsa -C GitHub邮箱地址`
- 进入`.ssh`目录，复制`id_rsa.pub`文件内容
- 登录GitHub。`Settings`  --> `SSH and GPG keys` --> `New SSH Key`
- 回到git通过ssh地址创建。`git remote add 别名 SSH地址`

## 5.3 多账户协作

配置 Windows 平台，使其在当前 Git 仓库中使用新的 GitHub 账号 `ydsama123`。

1. 生成 SSH 密钥
   首先，为你的新 GitHub 账号生成一个 SSH 密钥。如果你已经有一个，可以跳过这一步。

```bash
ssh-keygen -t ed25519 -C "YourNewGitHubEmail@example.com"
```

这会提示你输入保存密钥的文件路径。你可以使用默认路径或指定一个新的路径。例如：

```
Enter file in which to save the key (/c/Users/YourUsername/.ssh/id_ed25519): /c/Users/YourUsername/.ssh/id_ed25519_ydsama123
```

2. 添加 SSH 密钥到 GitHub
   将生成的公钥 (`id_ed25519_ydsama123.pub`) 添加到你的 GitHub 账号 `ydsama123` 中。你可以通过以下步骤完成：

3. 打开 GitHub 网站并登录到你的账号 `ydsama123`。
4. 进入 **Settings**。
5. 在左侧菜单中选择 **SSH and GPG keys**。
6. 点击 **New SSH key**，将 `id_ed25519_ydsama123.pub` 文件的内容复制粘贴到密钥框中，并保存。

7. 配置 SSH 文件
   创建或编辑 `~/.ssh/config` 文件，添加以下内容：

```
Host github.com-ydsama123
    HostName github.com
    User git
    IdentityFile /c/Users/YourUsername/.ssh/id_ed25519_ydsama123
```

确保路径 `/c/Users/YourUsername/.ssh/id_ed25519_ydsama123` 是你生成的密钥文件的实际路径。

4. 克隆仓库或修改现有仓库的远程 URL
   如果你还没有克隆仓库，可以使用以下命令克隆：

```bash
git clone git@github.com-ydsama123:ydsama123/testrepo.git
```

如果仓库已经克隆，可以修改现有仓库的远程 URL：

```bash
cd /path/to/your/repository
git remote set-url origin git@github.com-ydsama123:ydsama123/testrepo.git
```

5. 配置本地仓库的用户名和邮箱
   进入你的 Git 仓库目录，并配置该仓库专用的用户名和邮箱：

```bash
cd /path/to/your/repository
git config user.name "ydsama123"
git config user.email "YourNewGitHubEmail@example.com"
```

6. 测试 SSH 连接
   测试是否能通过 SSH 连接到 GitHub：

```bash
ssh -T git@github.com-ydsama123
```

如果配置正确，你应该会收到类似以下的消息：

```
Hi ydsama123! You've successfully authenticated, but GitHub does not provide shell access.
```

7. 使用新的配置进行 Git 操作
   现在，你可以在这个仓库中使用新的 GitHub 账号进行操作，如推送、拉取等：

```bash
git push origin main
```

通过以上步骤，你应该能够在当前 Git 仓库中使用新的 GitHub 账号 `ydsama123` 进行授权和认证，而不会影响到全局配置的 GitHub 账号。

# 6 Github工作流

## 6.1 Issue

GitHub Issue 是一个非常核心的功能，用于追踪和管理一个项目中的任务、缺陷、功能请求、或者其他工作项。Issue 可以帮助项目维护者和贡献者跟踪和讨论项目中的各种问题和改进点，从而提升项目的组织和协作效率。

### 如何使用 GitHub Issue

#### 1. 创建 Issue
- **打开 GitHub 项目主页**，点击 "Issues" 选项卡。
- 点击 "New issue" 按钮。
- 填写 Issue 的标题和详细描述。描述中可以使用 Markdown 格式化，还可以插入图片、链接等。
- 可以为 Issue 分配给特定的项目成员、标记标签（比如 bug、enhancement、help wanted 等）和关联到项目的里程碑。
- 创建完成后，点击 “Submit new issue” 提交。

#### 2. 管理 Issue
- **查看和筛选**：在 Issues 选项卡中，可以看到所有的 Issue。可以通过状态（如 open 或 closed）、标签、作者等进行筛选。
- **更新 Issue**：打开一个 Issue，可以通过评论来更新进展，或者修改 Issue 的状态和属性。
- **关闭 Issue**：任务完成后，可以点击 "Close issue" 来关闭一个 Issue。

#### 3. Issue 互动
- **评论**：项目的参与者可以在 Issue 下方添加评论来讨论问题。
- **@提及**：可以在评论中使用 `@username` 来提及特定用户，这样对方会收到提醒。
- **引用**：可以通过在评论中添加 Issue 或 Pull Request 的编号（如 `#123`）来引用其他 Issue 或 Pull Request。

### GitHub Issue 对项目的意义

1. **改进项目沟通**：Issue 提供了一个集中的讨论平台，项目相关的所有人可以在此讨论问题，确保信息的透明和流通。
2. **任务管理**：通过 Issue，项目维护者可以跟踪任务的进展状态，安排优先级，分配任务给特定的人。
3. **文档化决策过程**：所有的讨论和决策都会被记录在 Issue 中，新加入的项目成员可以通过阅读这些 Issue 来了解项目的历史和决策背景。
4. **集成自动化工具**：GitHub Issue 可以与其他服务（如 CI/CD 工具）集成，自动化处理一些常见的任务，如自动关闭 Issue、测试代码等。
5. **增强项目的可见性和参与度**：开放的 Issue 让更多的人了解项目的需要和缺陷，吸引更多的外部贡献者参与项目。



## 6.2 Pull Request

GitHub 的 Pull Request (PR) 是一个核心功能，用于在团队中协作和审查代码。当开发者完成一个功能开发或修复一个错误后，他们可以创建一个 Pull Request，请求将他们的代码从一个分支合并到另一个分支（通常是主分支）。这个过程中，其他团队成员可以查看、讨论和修改提议的代码，最终决定是否接受（合并）这些更改。

### 如何创建 Pull Request

1. **Fork 和 Clone 仓库**：
   - 首先，如果你没有写权限，需要先 Fork 目标仓库到你的 GitHub 账号下。
   - 然后，Clone 你的 Fork 到本地开发环境。

2. **创建新分支**：
   - 在本地仓库中创建一个新分支，通常基于最新的主分支。
   - 分支命名应具有描述性，如 `fix-login-bug` 或 `feature-add-search`。

3. **提交更改**：
   - 在新分支上进行代码更改。
   - 完成更改后，进行 commit，commit 信息应清晰描述所做的更改。

4. **推送分支到 GitHub**：
   - 使用 `git push` 命令将新分支推送到你的 GitHub Fork。

5. **创建 Pull Request**：
   - 在 GitHub 上，转到原始仓库（你 Fork 的仓库），你应该会看到一个提示，可以创建一个 Pull Request。
   - 点击 “Compare & pull request” 按钮。
   - 添加一个清晰的标题和详细的描述，解释你的更改和原因。
   - 确认 PR 要合并的目标分支，通常是原始仓库的 `main` 或 `master` 分支。
   - 提交 Pull Request。

6. **代码审查和讨论**：
   - 其他团队成员会审查 PR，并可能提出修改建议。
   - 根据反馈进行必要的修改，更新你的 Pull Request。

7. **合并 Pull Request**：
   - 一旦 PR 获得批准，并通过所有必要的自动化测试，项目维护者可以合并它到目标分支。

### Pull Request 的实践规范

1. **保持 PR 小而专注**：每个 PR 应只解决一个具体问题或添加一个功能，这样更易于审查和理解。
2. **写清楚的描述和标题**：标题应简洁明了，描述中详细说明为什么需要这些更改，如果关联到特定的 Issue，应包括 Issue 链接。
3. **遵循代码风格和标准**：确保你的代码遵守项目的编码标凈和风格指南。
4. **包含测试**：如果项目有测试框架，应添加测试来验证你的更改。
5. **及时响应反馈**：提交 PR 后，应积极参与讨论并对反馈做出响应。
6. **使用草稿 PR**：如果你需要早期反馈，可以先创建一个草稿 PR，然后在准备好后标记为 “Ready for review”。

通过遵循这些实践，你可以有效地使用 GitHub Pull Requests 来提高代码质量和团队协作效率。

## 6.3 Github Project

GitHub Projects 是 GitHub 提供的一个项目管理工具，旨在帮助用户组织和优先排序工作，跟踪和管理项目进度。这个工具能够与仓库紧密集成，使得管理问题（Issues）、拉取请求（Pull Requests）和注释等变得更加方便。

### GitHub Projects 的特点：

- **看板（Kanban）风格**：GitHub Projects 默认提供了类似看板的界面，可以创建多个列，如“待办”、“进行中”、“已完成”等，以可视化地跟踪任务的进展。
- **自动化功能**：可以设置自动化规则，例如当 Issue 被关闭时自动将其移动到“已完成”列。
- **集成**：直接与 GitHub Issues 和 Pull Requests 集成，允许你从项目视图中直接管理这些元素。
- **协作**：团队成员可以查看项目的状态，更新任务和提供反馈，促进团队协作。

### 如何管理 GitHub Project

#### 1. 创建一个 Project

- 转到 GitHub 仓库页面，点击 “Projects” 选项卡。
- 选择 “New project”。
- 填写项目名称、描述，并选择项目模板（如基本的 Kanban 模板）。
- 创建项目后，可以自定义添加所需的列，例如“待办”、“进行中”、“已完成”。

#### 2. 添加和管理任务

- 你可以直接在项目中创建新的任务（notes），或者将现有的 Issues 和 Pull Requests 添加到项目中。
- 拖放任务卡片来在不同的列之间移动，以更新任务的状态。
- 使用“+”按钮或直接将 Issue/Pull Requests 从仓库的 Issue 列表拖入特定列。

#### 3. 设置自动化

- 在项目页面，点击“Menu”（三个点）并选择“Manage automation”。
- 设置自动规则，例如当 Issue 被关闭时自动移动到“已完成”列。

#### 4. 监控和调整

- 定期检查项目进度，调整任务优先级和资源分配。
- 与团队成员进行定期的回顾和计划会议，确保所有人对当前进度和下一步行动有共同的理解。

#### 5. 利用里程碑和标签

- 利用 GitHub 的里程碑功能来管理具有特定期限的项目阶段。
- 使用标签来分类任务，如“bug”、“feature”等，便于过滤和搜索。

### 最佳实践

- **定期更新**：确保所有任务都保持最新状态，反映实际的工作进展。
- **明确责任**：为每个任务明确指定责任人，确保任务的负责性和可追踪性。
- **细分任务**：将大任务细分为可管理的小任务，使进度更容易跟踪和完成。
- **透明沟通**：使用项目的讨论区或相关 Issue 中的评论功能保持团队沟通。

使用 GitHub Projects，你可以更好地管理软件开发项目，保持团队的协调一致，同时提高工作效率和透明度。

## 6.4 Github Actions

GitHub Actions 是 GitHub 的一个自动化和 CI/CD（持续集成与持续部署）平台，允许开发者在 GitHub 仓库中自动执行软件开发工作流程。通过 GitHub Actions，你可以自动化测试、构建、部署等任务，而无需离开 GitHub 环境。

### GitHub Actions 的核心组件

- **工作流（Workflows）**：由一个或多个作业组成，定义了一系列的步骤和任务，这些任务可以被触发执行。
- **事件（Events）**：工作流可以通过各种事件触发，如推送（push）到仓库、发起拉取请求（pull request）、定时事件（cron）、等等。
- **作业（Jobs）**：工作流中的作业包含一系列的步骤，这些步骤可以在同一执行环境中运行或在不同的环境中并行运行。
- **步骤（Steps）**：每个作业中的步骤可以是执行命令或者是使用市场上的动作（actions）。
- **动作（Actions）**：可以复用的组件，允许你将逻辑封装为可在工作流中多次使用的单元。

### 如何使用 GitHub Actions

1. **创建工作流文件**：
   在你的 GitHub 仓库中，创建一个 `.github/workflows` 目录（如果还没有的话），然后在该目录下创建 YAML 格式的工作流文件，例如 `ci.yml`。

2. **定义工作流**：
   在 YAML 文件中定义工作流的触发事件、作业和步骤。

   ```yaml
   name: CI Workflow 
   on: [push, pull_request]  # 触发事件：在 push 或 pull_request 时触发
   
   jobs:
     build:
       runs-on: ubuntu-latest  # 执行环境
       steps:
         - uses: actions/checkout@v2  # 使用市场上的 action 检出代码
         - name: Install dependencies
           run: npm install  # 安装依赖
         - name: Run tests
           run: npm test  # 运行测试
   ```

3. **提交并推送更改**：
   将工作流文件提交到你的仓库。一旦触发事件发生，GitHub Actions 将自动执行定义的工作流。

### 如何编写 GitHub Actions 脚本

- **使用 Shell 命令**：在 `steps` 下的 `run` 字段中可以直接运行 shell 命令。
- **使用 Actions**：可以在步骤中使用现有的 Actions，如 `actions/checkout` 用于检出代码，或者你可以创建自己的 Actions。
- **环境变量和秘密（Secrets）**：可以通过环境变量或 GitHub 提供的 Secrets 管理敏感数据。

   ```yaml
   steps:
     - name: Deploy to server
       env:
         ENVIRONMENT: production
       run: |
         echo "Deploying to $ENVIRONMENT"
         deploy_script.sh
       secrets:
         PASSWORD: ${{ secrets.DEPLOY_PASSWORD }}
   ```

### 最佳实践

- **保持工作流的简洁性**：尽量使工作流简单易懂，避免复杂的依赖。
- **重用 Actions**：利用市场上的 Actions 来避免重复编写代码。
- **安全管理秘密**：使用 GitHub 的 Secrets 功能来安全地存储和使用敏感信息。
- **文档化**：为你的工作流添加适当的注释和文档，使其易于维护和理解。

通过这种方式，GitHub Actions 提供了一个非常强大且灵活的工具，可以大大提高软件开发和部署的效率。

## 6.5 协议与说明

### 6.5.1 README

GitHub 工作流中的 README 文件扮演着至关重要的角色，它不仅是项目的门面，也是向新用户、开发者或潜在贡献者介绍项目的首要工具。README 文件的内容和格式应当简洁明了，同时提供所有必要的信息以帮助人们理解、使用和参与项目。

README 文件的作用

1. **项目介绍**：简明扼要地介绍项目的目的和功能。
2. **快速启动指南**：提供足够的信息，使得新用户可以快速开始使用或开发项目。
3. **安装指导**：详细说明如何安装和配置项目。
4. **使用示例**：通过具体示例帮助用户理解如何使用项目的功能。
5. **贡献指南**：鼓励并指导外部开发者如何正确地贡献项目。
6. **许可证信息**：明确项目的使用和分发条款。
7. **联系方式**：提供维护者或团队的联系信息，以便于交流和协作。

内容和格式建议

标题和简介

- **项目名称**：应当突出且易于理解。
- **一句话描述**：简单介绍项目的核心功能或目的。

安装指南

```markdown
## 安装

提供详细的安装步骤：

```bash
git clone https://github.com/yourusername/yourprojectname.git
cd yourprojectname
pip install -r requirements.txt
```

请根据项目实际情况调整安装命令。
```

#### 使用说明

```markdown
## 使用

展示如何使用项目的基本命令或代码：

```python
import yourproject

yourproject.do_something()
```
```

#### 贡献指南

```markdown
## 贡献

鼓励开发者贡献，并提供链接到详细的贡献指南：

- 查看 [CONTRIBUTING.md](CONTRIBUTING.md) 来了解如何开始贡献。
- 提交 Pull Requests。
- 报告 Bugs。
```

许可证

```markdown
## 许可证

本项目采用 [MIT 许可证](LICENSE)。详情请查阅项目中的 LICENSE 文件。
```

联系方式

```markdown
## 联系方式

如有任何问题，可通过以下方式联系我们：

- 邮件：[contact@example.com](mailto:contact@example.com)
- GitHub Issue：[提交问题](https://github.com/yourusername/yourprojectname/issues)
```

结论

一个好的 README 文件不仅能够提升项目的专业形象，还能增加用户和开发者的信任和参与度。务必确保 README 既全面又简洁，便于用户快速获取他们需要的信息。

### 6.5.2 SECURITY

SECURITY 文件的定义和作用

在 GitHub 或其他代码托管平台上，`SECURITY.md` 文件是一个专门用于说明软件项目的安全政策和漏洞报告过程的文档。这个文件对于确保项目的安全性至关重要，它向用户和研究者提供了如何正确报告安全问题的指南。通过提供清晰的安全政策和报告流程，项目维护者可以更有效地管理和修复安全漏洞，同时与安全社区保持良好的互动。

组织 SECURITY 文件的内容

安全政策介绍

文件开头应简明扼要地介绍文件的目的和重要性，明确指出该文件的目的是提供一个标准的安全漏洞报告和处理流程。

```markdown
# 安全政策

欢迎来到 [项目名称] 的安全政策页面。在这里，我们提供关于如何报告安全漏洞的指南，以及我们处理这些问题的流程。
```

支持的版本

列出当前支持的版本，并明确说明哪些版本可以接收安全更新。

```markdown
## 支持的版本

下表列出了我们目前支持的版本。请确保您的系统运行的是支持的版本之一。

| 版本 | 支持状态 |
|------|----------|
| 1.0  | ✅        |
| 2.0  | ✅        |
| 2.5  | ❌        |
```

如何报告安全漏洞

详细说明用户如何安全地报告安全漏洞，包括使用的通信渠道（例如加密电子邮件、专有的报告工具等）。

```markdown
## 报告安全漏洞

如果您发现了安全漏洞，请通过以下方式与我们联系，不要在公共论坛（如GitHub issue等）上报告安全漏洞：

- 邮件：[security@example.com](mailto:security@example.com)
- 加密邮件（可选）：我们的 PGP 公钥在 [这里](链接到PGP密钥)

请提供尽可能详细的报告，包括复现步骤、影响范围以及您认为可能的修复方法。
```

安全漏洞处理流程

描述一旦接收到安全漏洞报告后的处理流程，包括评估、确认漏洞、修复以及如何通知用户。

```markdown
## 安全漏洞处理流程

1. **接收和确认报告**：我们会在24小时内确认收到您的报告，并在接下来的72小时内评估报告的严重性。
2. **问题调查**：我们的团队将调查并确定修复方案。
3. **修复和发布更新**：确定解决方案后，我们将尽快修复漏洞并发布更新。
4. **公开通信**：修复后，我们将通过适当的渠道公开通知所有用户，并提供必要的升级或补丁。
```

感谢

可选地，可以提供一个感谢部分，表扬那些负责任地报告安全问题的研究者。

```markdown
## 感谢

我们感谢所有负责任地报告安全问题的研究者。每个报告都帮助我们提高了项目的安全性。
```

### 6.5.3 LICENSE

许可证文件，说明项目的开源许可声明，详见许可证选择-blog

## 6.6 Wiki

GitHub 项目的 Wiki 是一个为 GitHub 项目提供文档的部分，它允许项目维护者和贡献者共同编写项目的相关文档。这些文档可以包括安装指南、使用说明、设计文档、常见问题解答等。Wiki 页面使用 Markdown 语法进行格式化，与其他 GitHub 文件类似。

### 如何使用 GitHub Wiki

#### 1. 开启 Wiki 功能
不是所有的 GitHub 项目都自动开启 Wiki 功能。项目拥有者需在项目的设置中手动开启：
- 打开 GitHub 项目主页。
- 点击右上角的 "Settings"。
- 在侧边栏中找到 "Features" 部分。
- 勾选 "Wikis" 以启用 Wiki 功能。

#### 2. 创建和编辑 Wiki 页面
一旦 Wiki 功能被启用，你可以开始添加和编辑页面：
- 在项目的主页上，点击 "Wiki" 选项卡。
- 初始时，你可能会看到一个 "Create the first page" 的提示，点击它来创建你的首个 Wiki 页面。
- 输入页面标题，并在下方的编辑框中使用 Markdown 或者 GitHub Flavored Markdown 语法编写内容。
- 完成编辑后，点击页面底部的 "Save Page" 按钮来保存页面。

#### 3. 管理 Wiki 页面
- **编辑已有页面**：打开任何一个 Wiki 页面，点击右上角的 "Edit" 按钮进行编辑。
- **添加新页面**：在 Wiki 首页点击 "New Page"。
- **查看历史和回退更改**：每个 Wiki 页面底部有 "Page History" 链接，允许查看该页面的所有修改历史，并可回退至任何一个旧版本。

#### 4. 克隆 Wiki
GitHub 的 Wiki 实际上是一个独立的 Git 仓库，你可以克隆这个仓库到本地，进行离线编辑和版本管理：
- 在 Wiki 页面，找到右侧的 "Clone this wiki locally" 链接。
- 使用 Git 命令克隆到本地，例如：
  ```bash
  git clone https://github.com/username/repository.wiki.git
  ```
- 本地编辑后，通过常规的 Git 流程（add、commit、push）将更改推回 GitHub。

#### 5. 设置访问权限
项目拥有者可以设置谁可以编辑 Wiki：
- 可以设为公共编辑，允许任何 GitHub 用户编辑。
- 也可以限制只允许项目的贡献者编辑。

Wiki 是一个非常适合团队合作和文档共享的功能，可以有效提升项目的透明度和可访问性。通过上述步骤，你可以轻松地开始使用 GitHub Wiki 来管理和分享你的项目文档。

## 6.7 发行版与标签

在 GitHub 中，**标签（Tags）** 和 **发行版（Releases）** 是用于标识特定项目状态的重要工具，通常与软件版本控制和发布过程相关联。

### 标签（Tags）

标签是附着在 commit 上的指针，通常用于表示项目中的重要点，如版本发布点。标签可以是轻量级的（仅是指向特定 commit 的引用），也可以是带注释的（存储更多的信息，如作者、邮件、日期和附加的消息）。

#### 创建标签

**在命令行中创建标签**：

1. **轻量级标签**:
   ```bash
   git tag v1.0.0
   ```

2. **带注释的标签**:
   ```bash
   git tag -a v1.0.1 -m "Release version 1.0.1"
   ```

**推送标签到 GitHub**:
```bash
git push origin v1.0.0         # 推送单个标签
git push origin --tags         # 推送所有标签
```

**在 GitHub 网站上创建标签**:
虽然 GitHub 网站界面直接不支持直接创建标签，但你可以在创建新发行版时自动创建新标签。

### 发行版（Releases）

发行版是基于 Git 标签的，它们为软件的特定状态提供了一个快照，并且通常包括预编译的软件、源代码包、编译说明和发行说明等。

#### 创建发行版

1. **进入你的 GitHub 仓库**。
2. 点击仓库顶部的 **Releases** 或 **Tags** 部分。
3. 点击 **Create a new release** 或在选定的标签旁边点击 **Draft a new release**。
4. 选择一个 Git 标签。如果需要创建新标签，你可以在此界面指定新标签名。
5. 填写发行版的标题和描述。
6. 如果需要，你可以将编译好的程序、源代码等作为附件上传。
7. 选择是否为预发布版或正式发布版。
8. 点击 **Publish release**。

### 最佳实践

- **版本命名**: 使用语义化版本命名约定（如 v1.0.2）来命名你的标签和发行版，使版本管理更加清晰。
- **详细发行说明**: 提供详细的发行说明，包括新功能、改进、修复的 bug 等，以便用户了解这一版本的变动。
- **保持一致性**: 对于标签和发行版的命名保持一致性，确保标签名称和发行版名称相匹配。

通过使用标签和发行版，你可以更有效地管理你的软件版本，使用户和开发者都能轻松地跟踪和获取特定版本的软件。
