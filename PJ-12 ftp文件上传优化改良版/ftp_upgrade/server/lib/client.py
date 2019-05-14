#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from server.conf import settings
import socket,struct,hashlib,os,json,time
import shelve
from lib import logger

# 客户端对象
class Client(object):
    MAX_PAKET = 8192
    def __init__(self):
        self.host = settings.host           # 远程主机地址，端口号
        self.family = settings.family       # 类型
        self.type = settings.prototal['tcp'] # 传输协议
        self.name_flag = 0                  # 作为判断发送用户数据，0表示未发送，1表示发送
        self.logobj = logger.mylog('client')
        self.shelveobj = shelve.open('.unfinished')
        self.status = {
            '100': 'login successed',
            '101': 'login failed',
            '102': 'incomplete data packet',
            '200': 'success operation',
            '201': 'data already exists',
            '202': 'not found the directory',
            '301': 'server failed operation',
            '401': 'keyword error',
            '402': 'the file’s md5 was by changed',
            '404': 'Incorrect commond',
            '501': 'not the same file',
            '502': 'esist the file',
            '503': 'your disk is full',
        }

    def create(self):
        """创建ftp客户端对象"""
        self.client = socket.socket(self.family,self.type)
        self.client.connect(self.host)
        self.logobj.info('create client')
        return self.client

    def _put(self,inp):
        """上传文件"""
        cmd,filename = inp
        if filename in os.listdir(os.getcwd()):
            self._format_request(inp)
            md5 = hashlib.md5()
            head = {}

            head['data-size'] = os.path.getsize(os.path.join(os.getcwd(),filename))
            md5.update(bytes(filename,'utf8'))
            head['md5'] = md5.hexdigest()
            head_bytes = bytes(json.dumps(head),'utf8')
            self.client.send(struct.pack('i',len(head_bytes)))
            self.client.send(head_bytes)
            progress = self.progress_bar(head['data-size'])
            progress.__next__()
            f = open(os.path.join(os.getcwd(),filename),'rb')

            cont = 0
            for line in f:
                self.client.send(line)
                cont += len(line)
                progress.send(cont)
            f.close()
            print(self.status[self.client.recv(100).decode('utf-8')]) # 返回传输的结果
            self.logobj.info('send file to server %s'%str(self.host))
        else:
            print('您本地路径下不存在此文件')
            self.logobj.error('curent directory haven’t the file')

    def _format_request(self,inp):
        """格式化打包数据并发送"""

        if len(inp) == 2:   # 如果终端命令是有多个字段数据的，比如put 1.txt
            dicts = {
                'type':inp[0],
                'data':inp[1]
            }
            self.client.send(json.dumps(dicts).encode('utf-8'))

        elif len(inp) == 1: # 如果终端命令只有单个字段时，即dir命令
            dicts = {
                'type':inp[0]
            }
            self.client.send(json.dumps(dicts).encode('utf-8'))


    def progress_bar(self,total_size,current_percent=0,last_percent=0):
        """进度条"""

        while True:
            received_size = yield current_percent
            current_percent = int(received_size/total_size *100)
            if current_percent > last_percent:
                print("#" * int(current_percent/2) + "{percent}%".format(percent=current_percent), end='\r',
                      flush=True)
                last_percent = current_percent  # 把本次循环的percent赋值给last

    def _get(self,inp):
        """下载文件"""
        cmd,filename = inp
        if filename in os.listdir(os.getcwd()):      # 检测本地文件是否已有同名文件
            print('您本地路径已经存在此文件')
        else:
            self._format_request(inp)
            struct_head_bytes_len = self.client.recv(10)   # 这里故意设置10，作返回状态用
            if len(struct_head_bytes_len) == 4:              # 当长度是4一定是返回的数据包
                head_len = struct.unpack('i',struct_head_bytes_len)[0]
                msg_dict = json.loads(self.client.recv(head_len).decode('utf-8',errors='ignore'))
                msg_md5 = msg_dict['md5']               # 接收到的文件md5值
                msg_size = msg_dict['data-size']

                md5 = hashlib.md5()
                md5.update(bytes(str(msg_size),'utf8'))      # 当前的md5值
                res = b''
                # 验证md5值
                if md5.hexdigest() == msg_md5:
                    file_path = os.path.join(os.getcwd(),filename)  # 本地路径
                    file_path = file_path.replace("\\",'/')
                    progress = self.progress_bar(msg_size)
                    progress.__next__()
                    f = open('%s.download'%file_path,'wb')
                    # 循环接收数据，并打印进度条
                    while len(res) < msg_size:
                        cont = self.client.recv(self.MAX_PAKET)             # 这个可以值在设置里修改
                        f.write(cont)
                        res += cont
                        recevied_size = len(res)
                        progress.send(recevied_size)
                        self.shelveobj[file_path] = [recevied_size,msg_size,msg_md5,'%s.download'%filename]
                            # 文件路径             已传输大小 总大小   md5   文件名
                        f.flush()
                    else:
                        f.close()
                        print('success')
                        os.rename('%s.download'%file_path,os.path.join(os.getcwd(),filename))
                        del self.shelveobj[file_path]
                        self.logobj.info('recv file  %s from server %s'%(filename,str(self.host)))
            else:   # 返回操作提示
                print(self.status[struct_head_bytes_len.decode('utf-8')])

    def _login(self):
        """登录函数"""
        datas = {}
        datas['username'] = input('username:').strip()
        datas['password'] = input('password:').strip()
        inp = ['auth',datas]
        self._format_request(inp)
        res = self.client.recv(1024).decode('utf-8')
        if res == '100':    # 返回状态100表示登陆成功
            print(self.status[res])
            self.logobj.info('user %s logined'%datas['username'])
            return True
        else:
            print(self.status[res])

    def _cmd(self,types):
        """终端命令函数"""
        self._format_request([types])
        struct_head_bytes_len = self.client.recv(1024)   # 这里为了获取切换目录的结果，刻意设置为100
        if len(struct_head_bytes_len) != 4:              # 返回切换目录创建目录等的结果
            print(struct_head_bytes_len)
            print(self.status[struct_head_bytes_len.decode('utf-8',errors='ignore')])
        else:   # 返回的数据包
            head_len = struct.unpack('i',struct_head_bytes_len)[0]
            msg_dict = eval(self.client.recv(head_len).decode('utf-8'))
            msg_len = msg_dict['data-size']
            res = b''
            while len(res) < msg_len:
                cont = self.client.recv(1024)
                res += cont
            # 检测当前操作系统的内核版本，并做针对性的打印输出
            if settings.system == 'nt':
                print(res.decode('gbk'))
            else:
                print(res.decode('utf-8'))
    def parser(self,inp):
        """解析用户输入并运行"""

        user_input_list = inp.split()    # 转为列表
        if len(user_input_list) == 2:    # 如果字段为2，即get cd put等命令
            types = user_input_list[0]
            if hasattr(self,'_%s'%types):
                func = getattr(self,'_%s'%types)
                func(user_input_list)
            else:
                print('不存在此方法')
                self.user_help()

        elif len(user_input_list) == 1:     # 如果字段为1，即dir/ls命令
            types = user_input_list[0]
            if types in ('put','get','cd'): # 排除用户输入命令不完整的情况
                self.user_help()
            else:
                self._cmd(types)

    def _cd(self,dirs):
        """切换服务器目录"""

        self._format_request(dirs)
        res = self.client.recv(100).decode('utf-8')
        print(self.status[res])

    def unfinished(self): # 未完成的任务事件
        """检测本地是否有未完成的任务"""

        if list(self.shelveobj.keys()):
            print('------ unfinished file list ------')
            for index,cont in enumerate(self.shelveobj.keys()):
                print('%s.\t\t已接收-%s\t总大小-%s\t文件名-%s'
                      %(index+1,self.shelveobj[cont][0],self.shelveobj[cont][1],self.shelveobj[cont][3]))
            while True:
                inp = input('序号：').strip()
                if not inp:continue
                elif inp in ('quit','exit'):break
                elif inp.isdigit():
                    inp = int(inp)-1    # 真实的序号
                    if inp >= 0 and inp <= index:
                        choice_file = list(self.shelveobj.keys())[inp]
                        print('you choice %s'%choice_file)
                        print('continue download...')
                        self._re_get(self.shelveobj[choice_file])
                        # if self.re_get(self.shelveobj[choice_file]):
                        #     # 当返回True表示操作成功，删除被操作对象
                        #     del self.shelveobj[choice_file]


    def _re_get(self,file):
        """断点续传"""
        inp = ['re_get',file]
        self._format_request(inp)
        filename = file[-1]     # 待续传的文件名
        filename = filename.replace('.download','')
        recevied_size = file[0] # 待续传的文件已接收的大小
        file_md5 = file[2]      # 待续传的文件md5值
        total_size = file[1]    # 待续传的文件总大小
        struct_head_bytes_len = self.client.recv(10)   # 这里故意设置1024，作返回状态用
        if len(struct_head_bytes_len) == 4:              # 当长度是4一定是返回的数据包
            head_len = struct.unpack('i',struct_head_bytes_len)[0]
            msg_dict = json.loads(self.client.recv(head_len).decode('utf-8',errors='ignore'))
            msg_md5 = msg_dict['md5']           # 发来的md5值
            msg_size = msg_dict['data-size']    # 发来的文件总大小

            if file_md5 == msg_md5 and total_size == msg_size:  # 验证是否是同一个文件
                file_path = os.path.join(os.getcwd(),'%s.download'%filename)
                file_path = file_path.replace('\\','/')
                f = open(file_path,'ab')
                f.seek(recevied_size)           # 走到已接收的字节数

                # 废弃的数据，因为已经有了
                self.client.recv(recevied_size)
                progress = self.progress_bar(msg_size,recevied_size,recevied_size)
                progress.__next__()

                # 循环接收数据，并打印进度条
                while recevied_size < msg_size:
                    progress.send(recevied_size)
                    cont = self.client.recv(self.MAX_PAKET)
                    f.write(cont)
                    recevied_size += len(cont)
                    f.flush()
                    # print('totaldata',msg_size)
                else:
                    f.close()
                    print('success')
                    self.logobj.info('re_get file from server %s'%str(self.host))
                    correct_name = os.path.join(os.getcwd(),filename)
                    correct_name = correct_name.replace('\\','/')
                    os.rename(file_path,correct_name)
                    del self.shelveobj[correct_name]

        else:   # 返回操作提示
            print(self.status[struct_head_bytes_len.decode('utf-8')])

    def user_help(self):
        """帮助方法"""

        d = '''
        get filename        -- download filename from server
        put filename        -- upload filename form server
        dir/ls              -- show current directory all file form server
        mkdir dirname      -- create document as the current directory from server
        cd  dirname        -- change curent directory as dir_name from server
        '''
        print(d)

    def run(self):
        """运行"""
        self.client = self.create()
        while True:
            if  not self.name_flag:      # 如果未登陆
                if self._login():        # 登陆成功
                    self.name_flag = 1   # 修改标志位为1
                    self.unfinished()    # 打印未完待续任务
            else:
                inp = input('>>>:').strip()
                if not inp:continue
                elif inp in ('quit','exit','q','e'):break
                self.parser(inp)    # 解析用户输入