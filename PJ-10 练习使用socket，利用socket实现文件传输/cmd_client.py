#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/2/4 0004 17:46

import socket,time

c = socket.socket()
address = ('127.0.0.1',8888)
c.connect(address)
while True:
    inp = input('>>>:')
    if inp == 'exit':break
    c.send(bytes(inp,'utf8'))
    data_len = int(str(c.recv(1024),'utf8')) #数据长度
    print('操作结果长度为：%s'%data_len)
    # time.sleep(1)
    c.send(bytes('test','utf8'))
    data = bytes()
    while  len(data) != data_len:
        data +=  c.recv(1024)
    print(str(data,encoding='gbk',errors='ignore'))
c.close()