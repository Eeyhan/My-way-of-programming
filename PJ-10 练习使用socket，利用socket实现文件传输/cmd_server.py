#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/2/4 0004 17:46
import socket,sys,subprocess

s = socket.socket()
address = ('127.0.0.1',8888)
s.bind(address)
s.listen(3)
conn,addr = s.accept()
while True:
    try:
        data = conn.recv(1024)
        # 拿到客户端传来的命令利用sub模块执行
        obj = subprocess.Popen(str(data,'utf8'),shell=True,stdout=subprocess.PIPE)
        result = obj.stdout.read()
        result_len = str(len(result)) #长度

        conn.sendall(bytes(result_len,'utf8'))  #发送长度
        conn.recv(1024)                         #阻塞
        conn.sendall(result)                    #发送真实数据
    except Exception as re:
        print(re)
        break
conn.close()