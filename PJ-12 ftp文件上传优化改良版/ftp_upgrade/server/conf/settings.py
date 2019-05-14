#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import logging
import os,sys,socket,json
# 默认根目录
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

# 用户数据路径
data_path = os.path.join(base_path,'db')

# 本地操作系统类型
system = os.name

# ftp 主机地址
host = ('127.0.0.1',8888)


# 服务器的family参数
family = socket.AF_INET

# 服务器协议
prototal = {
    'tcp':socket.SOCK_STREAM,
    'udp':socket.SOCK_DGRAM
}

# ftp 服务器工作根目录
server_path = os.path.join(base_path,'FTP_workstation')

# ftp用户远程家目录配置
f = open(os.path.join(data_path,'.userdata'))
data = json.load(f)
f.close()
remote_path = {}
for i in data:
    remote_path[i] = os.path.join(server_path,i)

listen = 10

# 日志级别
level = logging.INFO

# 日志文件分类处理
log_file ={
    'server':os.path.join(base_path,'log','server.log'),
    'client':os.path.join(base_path,'log','client.log')
}

# 日志格式
log_format = '%(asctime)s -- %(levelname)s -- %(filename)s -- %(message)s '


# 线程池数目
thread_num = 10