#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/2/3 0003 17:36

import socket

c = socket.socket()                 #创建socket对象
address = ('127.0.0.1',8800)        #设定ip和端口，必须和服务端的socket对象的ip和端口一致
c.connect(address)                  #连接设定的ip和端口

while True:
    data = input('>>>:')
    if data == 'exit':break
    c.send(bytes(data,'utf8')) #传输数据，并以bytes格式传
    recvdata = c.recv(1024)
    print(str(recvdata,'utf8'))

c.close()