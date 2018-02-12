#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/2/11 0011 22:18

import os

base_dir = os.path.dirname(__file__)    #默认根目录
transport_type = 'post'                 #传输方式
dir = 'test'                            #存放文件夹名,记得事先创建好
path = os.path.join(base_dir,dir)       #存放路径