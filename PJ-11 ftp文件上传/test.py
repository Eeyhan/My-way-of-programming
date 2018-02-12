#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/2/5 0005 16:31

# import socket,subprocess
# s = socket.socket()
# addr = ('127.0.0.1',8000)
# s.bind(addr)
# s.listen(3)
# conn,address = s.accept()
# while True:
#     res = conn.recv(1024)
#     if not res:
#         conn.close()
#         conn,addr = s.accept()
#         continue
#     data = subprocess.Popen(str(res,'utf8'),shell=True,stdout=subprocess.PIPE)
#     resdata = data.stdout.read()
#     res_len = len(str(resdata))
#     conn.send(bytes(res_len),'utf8')
#     conn.recv(1024)
#     conn.send(resdata)
# conn.close()
#
#
#
# import socket
# c = socket.socket()
# add = ('127.0.0.1',8000)
# c.connect(add)
# while True:
#     data = input('>>>:')
#     if data == 'exit':break
#     c.send(bytes(data,'utf8'))
#     res_len = int(str(c.recv(1024),'utf8'))
#     print('长度为；%s'%res_len)
#     c.send(' ')
#     data = bytes()
#     if len(data) != res_len:
#         data += c.recv(1024)
#     print(str(data,'gbk'))
# c.close()
