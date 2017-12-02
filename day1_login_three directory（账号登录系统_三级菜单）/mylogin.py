#-*- coding:utf-8 -*-

# import json
# data=json.loads(f.read().replace("'",'"'))  #将字符串里的单引号替换成双引号,带u'的字符串，u也要去掉
# print(type(data))
# f.close()

f=open('database.txt','r')
database=eval(f.read())
f.close()

f2=open('free.txt','r')
free=eval(f2.read())
f.close()

print('Welcome to login xx system/欢迎使用XX登录系统')
kw=input('您想注册账户/登录账户，注册请输入【R】键，登录请输入【L】键：')
if kw == 'R':#注册账户
    print('register account:')
    username=input('please enter your name/请输入您的账户名:')
    while  username in database.keys(): #如果昵称与已存在的账户名重复，提示重新取名
        print('The %s you entered already exists. Please enter a different one/您输入的%s已被使用，请输入其他帐户名'%(username,username))
        username=input('please enter your name/请输入您的账户名:')
    else:
        password=input('please enter your password/请输入您的密码:')
        while len(password)<8: #密码规则
            print('Your password is too simple, at least 8 digits. We recommend that you enter letters, numbers, special symbol combinations/您的密\
码过于简单，需要至少8位数，我们建议你输入字母，数字，特殊符号组合')
            password=input('please enter your password/请输入您的密码:')
        else:
            database[username]=password
            f=open('database.txt','w')
            f.write(str(database))
            f.close()
    print('Registered account success/注册账户成功')

count=3 #做为登录次数计数
temp=0  #临时变量
if kw == 'L':#登录账户
    print('login account:')
    username=input('please enter your name/请输入您的账户名:')
    password=input('please enter your password/请输入您的密码:')
    while count:
        if username in database.keys():
            if database[username]==password:
                print('登录成功')
                break
            elif database[username]!=password:
                count-=1
                print('密码错误，您还有%d次输入密码的机会'%count)
                password=input('please enter your password/请输入您的密码:')
            if  count <=1:
                temp=database.pop(username)
                f1=open('database.txt','w')
                f1.write(str(database))
                f1.close()

                free[username]=temp
                f2=open('free.txt','w')
                f2.write(str(free))
                f2.close()
                print('很抱歉，您的次数已用完，已将您的帐户冻结，解冻请联系管理员')
                break
        else:
            count-=1
            print('您输入的帐户名不存在或者已被冻结，请重新输入，您还有%d次输入账户的机会'%count)
            username=input('please enter your name/请输入您的账户名:')
            if  count <=1:
                print('很抱歉，您的次数已用完,程序将退出')
                break
if kw not in ('R','L'):
    print('输入有误')





