#!usr/bin/env python
#-*- coding:utf-8 -*-
# author:yangva


import socket,os
import settings

s = socket.socket()
address = ('127.0.0.1',8800)
s.bind(address)
s.listen(3)
base_dir = settings.base_dir

def recv():
    print('服务端启动....')

    conn,addr = s.accept()
    path = settings.path                            #设定待存放文件路径
    while True:
        info = str(conn.recv(1024),'utf8')          #接受文件名和文件大小
        if not info:
            conn.close()
            conn,addr = s.accept()
            continue
        filename,filesize = info.split(',')         #分割出文件名和文件大小
        print('待传输的文件大小为：%s'%filesize)
        print('请稍后....')
        f = open(os.path.join(path,filename),'wb')  #创建文件
        recv_size =0                                #已接受数据的值，初始为0
        while recv_size != int(filesize):           #循环接受数据，直到数据接收完整
            data = conn.recv(1024)                  #每次接受1024个字节
            f.write(data)                           #每接受1024个就写入文件
            recv_size += len(data)                  #每接受一次增加同等值的已接受值
        f.close()
        print('传输完成')
    s.close()
if __name__ == '__main__':
    recv()

