#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/2/11 0011 11:36

import socket
address = ('127.0.0.1',8888)
c = socket.socket()
c.connect(address)
print('客户端启动。。。')
while True:
    data = input('>>>:')
    c.send(bytes(data,'utf8'))
    if data == 'exit':break
    res_data = c.recv(1024)
    print(str(res_data,'utf8'))
c.close()