#!usr/bin/env python
#-*- coding:utf-8 -*-
# author:yangva

import socket,os
import settings
c = socket.socket()
addr = ('127.0.0.1',8800)
base_dir = settings.base_dir

def send():
    print('客户端启动...')
    c.connect(addr)

    types,filename = input('>>>:').strip().split('/')   #分割出输入的传输方式、文件名
    if types != settings.transport_type:exit()          #传输方式
    path = os.path.join(base_dir,filename)              #拼凑文件名的绝对路径
    filesize = os.stat(path).st_size                    #文件名的空间大小
    info = '%s,%s'%(filename,filesize)
    c.sendall(bytes(info,'utf8'))                       #传输文件名、文件大小

    sent_size = 0                                       #设定初始值，用于标记已传输的大小
    f = open(path,'rb')
    while sent_size != filesize:                        #循环传入，直到传完整个文件
        data = f.read(1024)                             #每次读取1024个字节大小
        if not data:break
        c.sendall(data)                                 #传输读取的1024个字节
        sent_size += len(data)                          #每传输一次增加同等值的已接受值
    c.close()
if __name__ == '__main__':
    send()