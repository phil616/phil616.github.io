# -*- coding:utf-8 -*-
import wx.adv
import wx
import os
import json
import re
import uuid

CONFIG_FILE = "config.json"

def construct_post_content(working_dir, title, c1,c2, tags, date, time, autogen):
    title = str(title)
    category = f"[{c1}, {c2}]"
    tags = ", ".join(tags)
    # date: wx.Datetime 
    # time: wx.Datetime
    filename = date.Format("%Y-%m-%d") + "-" + c2 + "-" + title + ".md"
    date = date.Format("%Y-%m-%d") + " " + time.Format("%H:%M:%S") + " +0800"
    autogen = str(autogen)
    content = f"""---
layout: post
title: {title}
categories: {category}
tags: [{tags}]
date: {date}
---
> AUTOGEN: {autogen}

# {title}

"""
    with open(os.path.join(working_dir, filename), 'w', encoding='utf-8') as f:
        f.write(content)
    return filename


WORKDING_DIR_NAME = ["_post", "_posts"]

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    return config

def locate_working_dir():
    scan_dirs = [".", "..", os.path.join("..","..")]
    for scan_dir in scan_dirs:
        for working_dir_name in WORKDING_DIR_NAME:
            working_dir = os.path.join(scan_dir, working_dir_name)
            if os.path.exists(working_dir):
                return os.path.join(scan_dir, working_dir_name)
                # return scan_dir + "/" + working_dir_name
    return None

editors = {
        "notepad": "C:/Windows/System32/notepad.exe",
        "notepad++": "C:/Program Files (x86)/Notepad++/notepad++.exe",
        "vscode": "C:/Program Files/Microsoft VS Code/Code.exe",
        "vscode-user": f"{os.environ['USERPROFILE']}/AppData/Local/Programs/Microsoft VS Code/Code.exe",
        "typora": "C:/Program Files/Typora/Typora.exe"
    }
def scan_editors():
    # supported editors: notepad, notepad++, vscode, typora
    # 查看各个编辑器是否在默认位置

    editors_path = []
    for editor_name, editor_path in editors.items():
        if os.path.exists(editor_path):
            editors_path.append(editor_name)
    return editors_path


class Frame(wx.Frame):
    def __init__(self, config, working_dir):
        _config = load_config()
        wx.Frame.__init__(self, None, title='Generator', size=(460, 600),name='frame',style=541072960)
        # icon = wx.Icon(r'C:\Project\phil616.github.io\assets\img\avatar.png')
        # self.SetIcon(icon)
        self.qdck = wx.Panel(self)
        self.qdck.SetOwnBackgroundColour((255, 255, 255, 255))
        self.Centre()
        self.bq1 = wx.StaticText(self.qdck,size=(80, 24),pos=(10, 10),label='博客生成器',name='staticText',style=2321)
        bq1_cjk_font = wx.Font(9,74,90,700,False,'Microsoft YaHei UI',28)
        self.bq1.SetFont(bq1_cjk_font)

        level_1_category = [item for item in _config['Category'].keys()] # 分类

        self.zhk1 = wx.ComboBox(self.qdck,value='',pos=(260, 189),name='comboBox',choices=level_1_category,style=16)
        self.zhk1.Bind(wx.EVT_COMBOBOX,self.on_select_category)

        self.zhk1.SetSize((150, 22))
        self.zhk2 = wx.ComboBox(self.qdck,value='',pos=(260, 259),name='comboBox',choices=[],style=16)
        self.zhk2.SetSize((150, 22))

        tags = _config['Tags']

        self.xzlbk1 = wx.CheckListBox(self.qdck,size=(90, 110),pos=(10, 160),name='listBox',choices=tags,style=0)
        self.bjk1 = wx.TextCtrl(self.qdck,size=(220, 24),pos=(100, 100),value='',name='text',style=0)
        self.bjk1.Bind(wx.EVT_TEXT,self.bjk1_nrbgb)
        self.sjk1 = wx.adv.TimePickerCtrl(self.qdck,size=(70, 24),pos=(130, 190),name='timectrl')
        self.sjk1.SetTime(21,46,5)
        self.bq2 = wx.StaticText(self.qdck,size=(80, 24),pos=(12, 100),label='输入标题',name='staticText',style=2321)
        self.bq3 = wx.StaticText(self.qdck,size=(100, 24),pos=(260, 159),label='选择一级分类',name='staticText',style=2321)
        self.bq4 = wx.StaticText(self.qdck,size=(100, 24),pos=(260, 229),label='选择二级分类',name='staticText',style=2321)
        self.bq5 = wx.StaticText(self.qdck,size=(80, 24),pos=(10, 130),label='标签',name='staticText',style=2321)
        bq5_cjk_font = wx.Font(9,74,90,700,False,'Microsoft YaHei UI',28)
        self.bq5.SetFont(bq5_cjk_font)
        self.bq7 = wx.StaticText(self.qdck,size=(80, 24),pos=(130, 130),label='时间',name='staticText',style=2321)
        bq7_cjk_font = wx.Font(9,74,90,700,False,'Microsoft YaHei UI',28)
        self.bq7.SetFont(bq7_cjk_font)
        self.rqk1 = wx.adv.DatePickerCtrl(self.qdck,size=(100, 24),pos=(130, 160),name='datectrl',style=2)

        supported_editors = scan_editors()
        
        self.fzdxk2 = wx.RadioBox(self.qdck,size=(300, 80),pos=(10, 300),label='可用的编辑器',choices=supported_editors,majorDimension=0,name='radioBox',style=4)
        if "typora" in supported_editors:
            self.fzdxk2.SetSelection(supported_editors.index("typora"))

        self.cjljk1 = wx.adv.HyperlinkCtrl(self.qdck,size=(60, 22),pos=(10, 520),name='hyperlink',label='代码仓',url=_config["Repo"],style=1)
        self.an3 = wx.Button(self.qdck,size=(420, 51),pos=(10, 430),label='新建',name='button')

        self.an3.Bind(wx.EVT_BUTTON,self.an3_nrbgb)  # 绑定按钮事件

        self.bq8 = wx.StaticText(self.qdck,size=(80, 24),pos=(10, 390),label='唯一标识',name='staticText',style=2321)
        self.bq9 = wx.StaticText(self.qdck,size=(80, 24),pos=(10, 40),label='配置文件加载',name='staticText',style=2321)
        bq9_cjk_font = wx.Font(9,75,90,400,False,'黑体',28)
        self.bq9.SetFont(bq9_cjk_font)
        self.bq10 = wx.StaticText(self.qdck,size=(80, 24),pos=(10, 70),label='目录加载',name='staticText',style=2321)
        bq10_cjk_font = wx.Font(9,75,90,400,False,'黑体',28)
        self.bq10.SetFont(bq10_cjk_font)
        self.bq11 = wx.StaticText(self.qdck,size=(80, 24),pos=(350, 100),label='标题可用',name='staticText',style=2321)
        self.bq11.SetForegroundColour((0, 0, 160, 255))
        self.bq12 = wx.StaticText(self.qdck,size=(80, 24),pos=(270, 130),label='选择分类',name='staticText',style=2321)
        bq12_cjk_font = wx.Font(9,74,90,700,False,'Microsoft YaHei UI',28)
        self.bq12.SetFont(bq12_cjk_font)
        autogen = uuid.uuid4().hex
        self.bq13 = wx.StaticText(self.qdck,size=(300, 24),pos=(100, 390),label=autogen,name='staticText',style=2321)
        self.bq14 = wx.StaticText(self.qdck,size=(220, 24),pos=(100, 70),label=config,name='staticText',style=2321)
        bq14_cjk_font = wx.Font(9,70,90,400,False,'宋体',28)
        self.bq14.SetFont(bq14_cjk_font)
        self.bq15 = wx.StaticText(self.qdck,size=(330, 24),pos=(100, 40),label=working_dir,name='staticText',style=2321)
        bq15_cjk_font = wx.Font(9,70,90,400,False,'宋体',28)
        self.bq15.SetFont(bq15_cjk_font)
        self.cjljk2 = wx.adv.HyperlinkCtrl(self.qdck,size=(60, 22),pos=(90, 520),name='hyperlink',label='博客官网',url=_config["Blog"],style=1)
        self.cjljk3 = wx.adv.HyperlinkCtrl(self.qdck,size=(60, 22),pos=(195, 520),name='hyperlink',label='关于',url=_config["About"],style=1)
        self.an5 = wx.Button(self.qdck,size=(90, 24),pos=(341, 65),label='打开配置文件',name='button')
        self.an5.Bind(wx.EVT_BUTTON,self.an5_nrbgb)  # 绑定按钮事件

    def on_select_category(self,event):
        selected = 'on_select_category', event.GetString()
        level_2_category = load_config()['Category'][selected[1]]
        self.zhk2.Clear()
        self.zhk2.AppendItems(level_2_category)

    def bjk1_nrbgb(self,event):
        # 标题输入框内容变化时触发
        val = self.bjk1.GetValue()
        # 正则判断是否出现闭合的 [] {} () 这种符号
        if re.search(r'[\[\{\(].*[\]\}\)]',val):
            self.bq11.SetForegroundColour((255, 0, 0, 255))
            self.bq11.SetLabel('标题不可用')
        else:
            self.bq11.SetForegroundColour((0, 0, 160, 255))
            self.bq11.SetLabel('标题可用')

    # self.an3 提交按钮被点击
    def an3_nrbgb(self,event):
        """
        print('an3,按钮被点击')
        print('标题：',self.bjk1.GetValue())
        print('一级分类：',self.zhk1.GetValue())
        print('二级分类：',self.zhk2.GetValue())
        print('标签：',self.xzlbk1.GetCheckedStrings())
        print('时间：',self.sjk1.GetValue())
        print('日期：',self.rqk1.GetValue())
        print('唯一标识：',self.bq13.GetLabel())
        print('编辑器：',self.fzdxk2.GetStringSelection())
        """
        # 打开编辑器
        filename = construct_post_content(
            working_dir = locate_working_dir(),
            title=self.bjk1.GetValue(),
            c1=self.zhk1.GetValue(),
            c2=self.zhk2.GetValue(),
            tags=self.xzlbk1.GetCheckedStrings(),
            date=self.rqk1.GetValue(),
            time=self.sjk1.GetValue(),
            autogen=self.bq13.GetLabel()
        )
        editor_type = self.fzdxk2.GetStringSelection()
        exec_path = editors[editor_type]
        command = "\"" + exec_path + "\""
        filepath = os.path.join(os.getcwd(),locate_working_dir(), filename)
        os.system(command + " " + filepath)
    def an5_nrbgb(self,event):
        os.startfile(CONFIG_FILE)
        
class myApp(wx.App):
    def  OnInit(self):
        config = load_config()
        if config is None:
            config = "未加载配置文件"
        else:
            config = f"已加载配置文件-{CONFIG_FILE}"
        work_dir = locate_working_dir()
        if work_dir is None:
            work_dir = "未找到工作目录"
        else:
            # os.path.abspath(work_dir)
            work_dir = "工作目录：" + str(os.path.abspath(work_dir))
        self.frame = Frame(config=config, working_dir=work_dir)
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    # 判断是否为windows系统
    if os.name != 'nt':
        exit()
    app = myApp()
    app.MainLoop()