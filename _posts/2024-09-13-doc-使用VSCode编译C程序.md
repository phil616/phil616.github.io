---
layout: post
title: 使用VSCode编译C/C++程序
categories: [Blog, Documents]
tags: [static]
date: 2024-09-13 23:43 +0800
---
> AUTOGEN c4df385010754f738ba97726d0c27968

# 使用VSCode配置编译C/C++单程序

除CMake等编译工具外，VSCode可以通过配置编译器等来为C、C++的单文件程序编译

## 使用.VSCode文件夹

- 打开命令面板（`Ctrl+Shift+P`）。
- 输入“Tasks: Configure Task”并选择它。
- 选择“Create tasks.json file from template”。
- 选择“Others”作为模板。
- 在生成的`tasks.json`文件中，配置构建任务。例如，使用GCC编译器的配置可能如下：

### 1. tasks

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "build C program",
            "type": "shell",
            "command": "gcc",
            "args": [
                "-g",
                "${file}", // 编译当前程序
                "-o",
                "${fileDirname}/${fileBasenameNoExtension}.out" // 输出的文件
            ],
            "group": {
                "kind": "build",
                "isDefault": true
            },
            "problemMatcher": [
                "$gcc"
            ]
        }
    ]
}
```

label是任务的名称

其中需要指定各个变量https://code.visualstudio.com/docs/editor/variables-reference

### 2. launch.json

- 打开命令面板（`Ctrl+Shift+P`）。
- 输入“Launch: Add Configuration...”并选择它。
- 选择“C++ (GDB/LLDB)”。
- 选择“cppdbg”作为调试器。
- 在生成的`launch.json`文件中，配置调试器。例如：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "(gdb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "program": "${fileDirname}/${fileBasenameNoExtension}.out", // 调试的程序
            "args": [],
            "stopAtEntry": false,
            "cwd": "${fileDirname}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                }
            ],
            "preLaunchTask": "build C program", // 构建任务的名称
            "miDebuggerPath": "/usr/bin/gdb", // gdb路径，根据系统实际情况修改
            "logging": {
                "trace": true,
                "engineLogging": true,
                "traceResponse": true
            },
        }
    ]
}
```

preLaunchTask与label相同

### tasks.json解释

- `version`: 指定了任务配置文件的格式版本。

- ```
  tasks
  ```

  : 一个数组，包含了所有的任务配置。

  - `label`: 任务的名称，用于在VSCode中显示。

  - `type`: 任务的类型，这里使用的是`shell`，表示任务会在一个shell环境中执行。

  - `command`: 要执行的命令，这里是`gcc`，表示使用GCC编译器。

  - ```
    args
    ```

    : 传递给命令的参数数组。

    - `"-g"`: 告诉编译器生成调试信息。
    - `"${file}"`: 一个变量，表示当前打开的文件的路径。
    - `"-o"`: 指定输出文件的名称。
    - `"${fileDirname}/${fileBasenameNoExtension}"`: 一个变量，表示输出文件的路径和名称，其中`${fileDirname}`是文件所在的目录，`${fileBasenameNoExtension}`是文件的基本名称，不包含扩展名。

  - group

    : 指定任务的组和是否是默认任务。

    - `"kind": "build"`: 表示这是一个构建任务。
    - `"isDefault": true`: 表示这是默认的构建任务。

  - `problemMatcher`: 用于匹配编译过程中可能出现的问题。

### launch.json解释

- `version`: 指定了调试配置文件的格式版本。

- ```
  configurations
  ```

  : 一个数组，包含了所有的调试配置。

  - `name`: 调试配置的名称，用于在VSCode中显示。

  - `type`: 调试器的类型，这里使用的是`cppdbg`，表示这是一个C++调试器。

  - `request`: 调试会话的请求类型，这里使用的是`launch`，表示启动一个新的调试会话。

  - `program`: 要调试的程序的路径，这里使用`${workspaceFolder}/${fileBasenameNoExtension}`表示工作区中当前文件的基本名称。

  - `args`: 传递给程序的参数数组，这里是空数组，表示没有参数。

  - `stopAtEntry`: 表示是否在程序入口处停止。

  - `cwd`: 程序的工作目录，这里使用`${workspaceFolder}`表示工作区的根目录。

  - `environment`: 程序运行时的环境变量数组。

  - `externalConsole`: 表示是否使用外部控制台。

  - `MIMode`: 调试器的模式，这里使用的是`gdb`。

  - ```
    setupCommands
    ```

    : 在调试会话开始前执行的命令数组。

    - `"description"`: 命令的描述。
    - `"text"`: 要执行的命令。
    - `"ignoreFailures"`: 表示是否忽略命令执行失败。

  - `preLaunchTask`: 调试会话开始前执行的构建任务的名称。

  - `miDebuggerPath`: 调试器的路径，这里使用的是`/usr/bin/gdb`，表示GDB调试器的路径。

  - logging

    : 调试日志的配置。

    - `"trace"`: 是否记录调试会话的详细日志。
    - `"engineLogging"`: 是否记录调试引擎的日志。
    - `"traceResponse"`: 是否记录调试器的响应。

  - `pipeTransport`: 用于远程调试的管道传输配置。
