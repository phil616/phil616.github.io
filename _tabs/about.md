---
# the default layout is 'page'
icon: fas fa-info-circle
order: 4
---

# 关于

关于此博客 


1. 博客搭建基于[Jekyll](https://jekyllrb.com/)构建，部署在Github Pages上。
2. 主题基于[Chirpy](https://github.com/cotes2020/jekyll-theme-chirpy)
3. 除特殊说明，其内容均属原创，按照[署名-非商业性使用-相同方式共享 4.0 国际](https://creativecommons.org/licenses/by-nc-sa/4.0/)协议进行许可。作者保留署名权，但要求署名时注明出处。
4. 博客内容另行标注的除外。
5. 博客内容仅供学习参考，请勿用于商业用途。作者不承担由于不遵守上述协议而导致的法律责任。
6. 博客交互内容采用Github API，详情参考Github政策。
7. 元信息链接为： [{{ site.url }}/meta/]({{ site.url }}/)，接入信息已经签名，安全可信。

## Quick Post

使用快速生成[Quick Post Page](https://phil616.github.io/assets/qp.html)，可以生成符合格式的模板，加入到Github中即可。

## 目录结构
本文档的目录结构如下：
1. Academy (绿荫学院)
   * Courses (课程)
   * CPC (马克思相关课程)
   * Adavanced (调查员培训)
2. Blog (博客)
   * Articles (文章)
   * Devops (运维)
   * Documents (文档)
   * Tips (技巧)
   * Questions (问题解答)
3. CyberSecurity (网络安全)
   * Report (报告)
   * General (常规)
   * Technology (技术)
4. AI (人工智能)
   * General (常规)
   * Courses (课程)
5. Guidence (指南)
   * Cpp (C/C++相关)
   * Python (Python相关)
   * Java (Java相关)
   * Web (Web相关)



## 作者联系方式
1. 邮箱

phil616@greenshadecapital.com

phil616@163.com
2. PGP

GSDispatch(Verified): dispatch@greenshadecapital.com [GreenShadeCapitalDispatchPubkey](https://keyserver.ubuntu.com/pks/lookup?search=4B45D9EB932D8D130778DD89CA557C41FE3EA9DF&fingerprint=on&op=index)

phil616(Verified): phil616@greenshadecapital.com: [GreenShadeCapitalPersonalPubkey](https://keyserver.ubuntu.com/pks/lookup?search=C508897F9A12BFFF2E5D6AF65F0BEAEF7AB20C87&fingerprint=on&op=index)

## AUTOGEN字段

AUTOGEN字段是在每个文章前自动生成的唯一标识符，用于在搜索引擎中检索字段。

由于博客内容不接入索引系统，因此使用唯一标识的AUTOGEN来实现在Google上面的唯一搜索

例如在`Linux-连接OpenVPN服务`一文中，可以直接使用AUTOGEN字段来在Google中搜索该文章

![image-20240917065827631](./../assets/img/about/image-20240917065827631.png)

能保障搜索结果唯一且存在

同理在Github中也可检索到唯一结果

![image-20240917065714575](./../assets/img/about/image-20240917065714575.png)



AUTOGEN可用被有限状态自动机识别，在生成格式中，AUTOGEN严格遵循如下表达式：

```
---
> AUTOGEN xxx
```

文件开头为YAML-FRONT-MATTER头部，结尾的三个短线后紧跟换行，随后是引用标识符`>`后接一个空格，随后是32位的唯一字符串

提取AUTOGEN字段的正则表达式参考：

```
\s*---\r?\n> AUTOGEN ([a-fA-F0-9]{32})
```

1. TAB栏没有AUTOGEN字段，因为TAB栏无法使用Service Worker更新
2. AUTOGEN字段在文章生成前自动生成

## 域名

url: phil616.greenshadecapital.com (2024年8月10日申请)

可在 [`phil616.greenshadecapital.com/CNAME`](https://phil616.greenshadecapital.com/CNAME)中查看CNAME

可在 [`phil616.greenshadecapital.com/GSCMESSAGE.txt`](https://phil616.greenshadecapital.com/GSCMESSAGE.txt)中查看授权证书

## 博客状态

1. Github 仓库： [GithubPage](https://github.com/phil616/phil616.github.io)
2. Github Page构建状态： [Actions](https://github.com/phil616/phil616.github.io/actions/)
3. License: MIT, GSE, Creative Commons
4. Green Shade API: [GreenShadeOpenAPI](https://api.greenshadecapital.com)
5. API Status: Not Online

## 举报

1. 违规和非法举报： inspection@greenshadecapital.com
2. 维权和法律相关： legal@greenshadecapital.com

> 若内容有争议或可能涉及其他非法行为，请向`consult@greenshadecapital.com`进行咨询。
{: .prompt-info }


> 2024-9-17