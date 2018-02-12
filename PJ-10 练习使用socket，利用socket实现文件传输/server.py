#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/2/3 0003 17:36

import socket

s = socket.socket()             #创建socket对象
address = ('127.0.0.1',8800)    #设定ip和端口
s.bind(address)                 #将socket对象绑定到设定的ip和端口
s.listen(3)                     #设置监听量为3，表示允许同时3个客户端连接
print('waiting......')
conn,addr = s.accept()          #接受TCP连接并返回conn,addr,其中conn是新的套接字对象(客户端的)，address是连接客户端的地址

while 1:
    try:
        data = conn.recv(1024)          #设定一次接收客户端socket传来最大的数据量
    except Exception as re:
        print(re)
        break
    else:
        print(str(data,'utf8'))
        #当客户端发来空信息，关闭客户端连接，重新获取新的连接

        if not data:
            conn.close()
            conn,addr = s.accept()
            continue

        inp = input('>>>:')
        conn.send(bytes(inp,'utf8'))


s.close()
