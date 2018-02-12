#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva

import socketserver

class myserver(socketserver.BaseRequestHandler):
    def handle(self):                               #这里的方法名是固定的，不能是其他的
        print('服务端启动。。。')
        while True:
            conn = self.request                     #和conn，addr = socket.accept()等同
            print(self.client_address)
            while True:
                client_data = conn.recv(1024)       #接受数据
                print(str(client_data,'utf8'))      #转为字符串
                req = input('>>>:')                 #输入数据
                conn.sendall(bytes(req,'utf8'))     #发送数据
            conn.close()

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1',8888),myserver)
    server.serve_forever()                          #服务永远存在，不关闭

