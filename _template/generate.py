import tkinter as tk
from tkinter import ttk
import subprocess

import os
import datetime
import uuid
import json


class DB:
    def __init__(self, filename):
        self.filename = filename
        try:
            with open(self.filename, encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {}
    def save(self):
        with open(self.filename, 'w', encoding="utf-8") as f:
            json.dump(self.data, f)

    def set(self,k,v):
        self.data[k] = v
    def get(self,k):
        return self.data[k]
    
    def has(self,k):
        return k in self.data

db = DB('db.json')

typora_path = "\"C:\\Program Files\\Typora\\Typora.exe\""

def looking_dir():
    current = os.path.join(os.path.dirname(os.path.abspath(__file__)),"_posts")
    parent = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"_posts")
    print(current)
    print(parent)
    if os.path.exists(current):
        return current
    elif os.path.exists(parent):
        return parent
    else:
        return None
def get_categories(one,two):
    target_top = one.split(" ")[0]
    target_buttom = two.split(" ")[0]
    establish_mapping = {
        "Academy":{
            "b101":"[Academy, Courses]",
            "b102":"[Academy, Courses]",
            "a101":"[Academy, AdvancedCourses]",
            "a102":"[Academy, AdvancedCourses]",
            "a103":"[Academy, AdvancedCourses]",
        },
        "CyberSecurity":{
            "cs":"[CyberSecurity, General]",
            "csr":"[CyberSecurity, Report]",
            "cst":"[CyberSecurity, Technology]",
        },
        "AI":{
            "ai":"[AI, General]",
            "aic":"[AI, Courses]",
        },
        "Blog":{
            "dev":"[Blog, Devops]",
            "doc":"[Blog, Documents]",
            "art":"[Blog, Articles]",
            "tip":"[Blog, Tips]",
            "ques":"[Blog, Questions]"
        },
        "Guidance":{
            "java":"[Guidance, Java]",
            "cpp":"[Guidance, Cpp]",
            "python":"[Guidance, Python]",
            "js":"[Guidance, JavaScript]",
            "web":"[Guidance, Web]"
        }
    }
    try:
        classes = establish_mapping[target_top][target_buttom]
        return classes
    except Exception:
        return "[Default]"

def get_tags(tag_list):
    if tag_list == []:
        return "[]"
    return "[" + ",".join(tag_list) + "]"


def get_filename(two,title):
    return datetime.datetime.now().strftime("%Y-%m-%d") + "-" + two.split(" ")[0] + "-" + title + ".md"

def get_datetime():
    return  datetime.datetime.now().strftime("%Y-%m-%d %H:%M +0800")

def render_markdown(title:str,category,tags,uid):

    starter = "---\n"
    starter += "layout: post\n"
    starter += "title: " + title + "\n" 
    starter += "categories: " + category + "\n"
    starter += "tags: " + tags + "\n"
    starter += "date: " + get_datetime() + "\n"
    starter += "---\n"
    starter += "> AUTOGEN " + uid + "\n"
    
    return starter
def check_post_dir():
    c = os.path.join(os.path.dirname(os.path.abspath(__file__)),"_posts")
    if os.path.exists(c):
        return "目录可用"
    else:
        return "目录不可用"

def on_button_click():
    # 获取输入框的内容
    input_text = input_entry.get()
    input_text = input_text.encode("utf-8")
    input_text = input_text.decode("utf-8")
    # 获取下拉框选择的值
    selected_option1 = option_var1.get()
    selected_option2 = option_var2.get()
    
    # 获取单选框选择的值
    selected_radio = radio_var.get()
    
    # 获取复选框选择的值
    selected_checkboxes = [var.get() for var in checkbox_vars]
    selected_tags = []
    for i in range(len(selected_checkboxes)):
        if selected_checkboxes[i]:
            selected_tags.append(tag_vars[i])
    categories = get_categories(selected_option1, selected_option2)
    uid = uuid.uuid4().hex
    markdown = render_markdown(input_text,categories,get_tags(selected_tags),uid)
    filename = get_filename(selected_option2,input_text)
    if db.has(filename):
        print("文件已存在")
    else:
        db.set(filename,uid)
    filepath = os.path.join(post,filename)
    f = open(filepath,"w",encoding="utf-8")
    f.write(markdown)
    f.close()
    db.save()
    if selected_radio == "rawtext":
        exit(0)
    elif selected_radio == "typora":
        command = typora_path +" " + filepath
        subprocess.Popen(command)
        return
        exit(0)
        
    else:
        return
        exit(0)

# 创建主窗口
window = tk.Tk()

window.geometry("300x500")

# 设置窗口标题
window.title("Quick Post")

pwd = os.path.dirname(os.path.abspath(__file__))
post = looking_dir()
if not post:
    print("没有找到 _posts 目录")
    exit(1)
notice_label = ttk.Label(window, text=f"文章目录有效 - {post}")
notice_label.pack()

# 创建输入框
input_label = ttk.Label(window, text="输入标题")
input_label.pack()
input_entry = ttk.Entry(window)
input_entry.pack()

# 创建下拉框
option_label = ttk.Label(window, text="选择文章类型")
option_label.pack()

option_var1 = tk.StringVar()
option_combobox1 = ttk.Combobox(window, textvariable=option_var1)
option_combobox1['values'] = ('Academy 绿荫学院', 'CyberSecurity 网安', 'AI 人工智能', 'Blog 博客', 'Guidance 课程', 'Other 其他')
option_combobox1.pack()

option_label2 = ttk.Label(window, text="选择具体类型")
option_label2.pack()

option_var2 = tk.StringVar()
option_combobox2 = ttk.Combobox(window, textvariable=option_var2)
option_combobox2.pack()

def update_options(*args):
    if option_var1.get() == 'Academy 绿荫学院':
        option_combobox2['values'] = ('b101 基础课', 'a101 经济课程')
    elif option_var1.get() == 'CyberSecurity 网安':
        option_combobox2['values'] = ('cs 网络安全', 'csr 网络安全报告', 'cst 网络安全技术')
    elif option_var1.get() == 'AI 人工智能':
        option_combobox2['values'] = ('ai 人工智能', 'aic 人工智能课程')
    elif option_var1.get() == 'Blog 博客':
        option_combobox2['values'] = ('dev 运维', 'doc 文档', 'art 文章', 'tip 技巧', 'ques 问答')
    elif option_var1.get() == 'Guidance 课程':
        option_combobox2['values'] = ('java Java', 'cpp C++', 'python Python', 'js JavaScript', 'web Web')
    else:
        option_combobox2['values'] = ('other 其他')
option_var1.trace_add('write', update_options)

# 创建单选框
radio_label = ttk.Label(window, text="单选框:")
radio_label.pack()

radio_var = tk.StringVar()
radio_button1 = ttk.Radiobutton(window, text="不打开编辑器", variable=radio_var, value="rawtext")
radio_button1.pack()
radio_button2 = ttk.Radiobutton(window, text="使用Typora", variable=radio_var, value="typora")
radio_button2.pack()

# 创建复选框
checkbox_label = ttk.Label(window, text="常用标签:")
checkbox_label.pack()

checkbox_vars = []
tag_vars = ['gs','static','memo','project','web']
for tag in tag_vars:
    var = tk.BooleanVar(name=tag)
    checkbox = ttk.Checkbutton(window, text=f"{tag}", variable=var)
    checkbox.pack()
    checkbox_vars.append(var)
# 创建按钮
button = ttk.Button(window, text="创建文件", command=on_button_click)
button.pack()

# 运行主循环
window.mainloop()
# pyinstaller --onefile generate.py --runtime-tmpdir .