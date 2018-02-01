#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/31 0031 15:43

import getpass
from libs.main import Admin

def initalize():
    try:
        user = input('请输入初始化用户名：')
        pwd = input('请输入初始化密码：')
        obj = Admin(user,pwd)
        obj.save()
        return True
    except Exception as e:
        print(e)

def main():
    show = '''
        1.初始化管理员帐户

        '''
    choice_dict = {
        '1':initalize
    }
    while True:
        print(show)
        choice = input('请输入操作选项：')
        if choice not in choice_dict:
            print('选项错误，请重新输入！')
        func =choice_dict[choice]
        if func():
            print('操作成功')
            return
        else:
            print('操作异常，请重新操作！')

