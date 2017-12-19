#!usr/bin/env python
#-*- coding:utf-8 -*-
# author:yangva
# datetime:2017/12/19 0018 14:10

#下面的json转换数据你可以继续使用eval,但是遇到编码问题等等的，eval就有些局限了
import json
with open('官方登录.txt') as f1,open('QQ登录.txt') as f2,open('微信登录.txt') as f3:
    gf_data = json.load(f1)
    qq_data = json.load(f2)
    wx_data = json.load(f3)
login_status = False  #标志位，登录状态参数
def login(auth_type):
    def wrapper(func):
        def inner():
            global login_status
            if login_status == False:
                if auth_type == 'guanfang':
                    print('官方登录模式，请登录')
                    user = input('username:')
                    pwd = input('password:')
                    if user in gf_data and pwd == gf_data[user]:
                        print('登录成功！')
                        login_status = True
                        return func()
                    else:
                        return '您输入的账户或密码有误'
                elif auth_type == 'QQ':
                    print('QQ登录模式，请登录')
                    user = input('username:')
                    pwd = input('password:')
                    if user in qq_data and pwd == qq_data[user]:
                        print('登录成功！')
                        login_status = True
                        return func()
                    else:
                        return '您输入的账户或密码有误'
                elif auth_type == 'weixin':
                    print('微信登录模式，请登录')
                    user = input('username:')
                    pwd = input('password:')
                    if user in wx_data and pwd == wx_data[user]:
                        print('登录成功！')
                        login_status = True
                        return func()
                    else:
                        return '您输入的账户或密码有误'
                else:
                    print('不存在的认证类型')
            else:
                return func()
        return inner
    return wrapper

@login('guanfang') #home = login(home)
def home():
    return '欢迎访问主页'
@login('weixin')
def electronic_digital():
    return '欢迎访问电子数码页'
@login('QQ')
def dress():
    return '欢迎访问服饰页'
@login('weixin')
def account():
    return '欢迎访问您的个人账户页'
@login('guanfang')
def shopping_cart():
    return '欢迎访问您的购物车页'
while True:
    print('1.主页\n2.数码产品\n3.服饰\n4.账户信息\n5.购物车\n6.退出')
    page = input('请选择访问页面（输入前面的序号即可）：')
    if page == '1':
        print(home())
    elif page == '2':
        print(electronic_digital())
    elif page == '3':
        print(dress())
    elif page == '4':
        print(account())
    elif page == '5':
        print(shopping_cart())
    elif page == '6':
        print('您已退出')
        break
    else:
        print('输入有误！！')