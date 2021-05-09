# 概述

本章针对初学者，用于快速搭建 python 环境，熟悉基本使用。

## 环境搭建
1. 安装 [vscode](https://code.visualstudio.com/Download) 
2. 安装 [python3.9](https://www.python.org/downloads/release/python-395/)
3. 阅读 [命令行界面](https://baike.baidu.com/item/%E5%91%BD%E4%BB%A4%E8%A1%8C%E7%95%8C%E9%9D%A2/9910197?fromtitle=CLI&fromid=2898851) ，了解基本概念。

## REPL
1. 打开控制台
   * windows 在开始的搜索框查找 `cmd`
   * mac 采用 `⌘空格键` ,唤起 [Spotlight](https://support.apple.com/zh-tw/guide/mac-help/mchlp1008/mac), 输入 `terminal` 打开命令行工具
2. 在控制台中输入 `python3.9`, 会唤起如下界面 (显示的版本号和时间等可能不同)
   
   ```
    Python 3.9.4 (default, Apr  5 2021, 01:49:30) 
    [Clang 12.0.0 (clang-1200.0.32.29)] on darwin
    Type "help", "copyright", "credits" or "license" for more information.
    >>> 
   ```
3. 此时可以输入 `1+1`，然后回车，会返回结果 2
   
   ```
   >>> 1+1
   2
   ```

   > 可以将此环境作为计算器使用，尝试输入其他数学表达式，按回车，查看结果。
4. 执行 `1 + _` 此时会返回 `3`, **_** 表示上次计算的结果
   
   ```
   >>> 1+1
   2
   >>> 1+_
   3
   ```
5. 除了作为计算器，你也可以执行代码。输入 `print('hello world!')` 回车，会输出
   
   ```
   >>> print('hello world!')
   hello world!
   ```
6. 输入 `quit()` 退出环境

::: tip
该环境可以反复循环的读取输入、执行、并打印结果。这样的交互式环境叫做 **REPL**(read-eval-print loop), 一般利用该环境实现快速代码验证等功能。
:::

### 快捷键
快捷键 |  功能
:---|:---|
↑|返回上一条执行命令，没有则停止
↓|返回下一条执行命令，没有则停止
回车键|执行输入的命令
tab|自动补全(只针对内置的函数名和变量等有效)
ctrl-l|清空屏幕
ctrl-z|windows 退出 **REPL**
ctrl-d|mac(类 Unix 系统) 退出 **REPL**
ctrl-a|移动到一行的开头
ctrl-e|移动到一行的结尾

::: tip
python REPL 中支持了 [GNU](https://baike.baidu.com/item/GNU) [Readline](https://tiswww.case.edu/php/chet/readline/readline.html#SEC_Contents) 单行文本编辑器的常用功能，阅读 [Readline Interaction](https://tiswww.case.edu/php/chet/readline/readline.html#SEC3) 详细了解
:::

## python命令
除了使用 `python3.9` 唤起 **REPL** 环境，也可直接使用 `python3.9` 命令执行代码。

1. 确保已退出 `REPL` 模式
2. 在控制台窗口输入 `python3.9 -c "print(1+1)"` 此时，控制台会输出 `2`

也可直接利用命令行执行文件

1. 创建 `print.py` 文件，编写如下内容
  
   <<<./examples/tutorial/print.py

2. 运行 `python3.9  print.py`，执行输出如下结果
   
   ```
   3
   hello world!
   ```

python3.9 详细使用参考 [python 文档](https://docs.python.org/3/using/cmdline.html#using-on-general)

## 源码格式
python 解释器在 2 和 3 中存在显著区别。
在 python2 中采用的是 [ASCII](https://baike.baidu.com/item/ASCII) 处理的源码文件，而 ASCII 字符集并不支持中文，所以在源码中包含中文时会报错。而在 python3 中默认字符集为 [utf-8](https://baike.baidu.com/item/UTF-8) 不存在上述问题。

一般可在源码开头申明 `# -*- coding: encoding -*-` 内容告知 python 解释器，采用 `utf-8` 格式解析源码。具体说明详见 [codes](https://docs.python.org/3/library/codecs.html#module-codecs)

## 知识点
1. [REPL](#repl) 用于快速验证 python 代码
   1. 熟记 [快捷键](#快捷键) 方便日常使用
   2. `_` 表示上次运算的结果
2. 采用 `python` 命令行执行命令
   1. `python -c "print(1 + 1)"` 执行字符串
   2. `python <文件名>` 执行文件
3. python2 由于默认采用 `ASCII` 解析源码，python3 使用 `utf-8`，为了避免 `python2` 默认解析中文时报错，在源码开头定义 `# -*- coding: utf_8 -*-` 避免解析错误。
