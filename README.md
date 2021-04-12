# 头歌平台自动签到脚本-无需知道签到码

本脚本仅供学习交流使用，请勿用于非法用途。

无意间发现，学校老师用的头歌平台的签到码居然是直接明文写到`json`中的，为了学习和锻炼，于是就有了这个脚本。

## 功能实现

1. 自动等待签到开始，并自动签到，无需知道签到码
2. 查询历史签到

## 演示

![signin](https://cdn.jsdelivr.net/gh/easechen/blog-img/img/20210412215956.gif)

## 所需的库

- requests

## 使用方法

首先安装所需的库

~~~bash
pip install requests
~~~

下载`src/sign.py`，运行即可

~~~bash
python sign.py
~~~

如果不想输入的话，直接在文件开头把账户和密码填入，再注释下面的输入函数即可。