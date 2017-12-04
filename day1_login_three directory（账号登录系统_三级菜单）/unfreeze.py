#-*- coding:utf-8 -*-

f=open('database.txt','r')
database=eval(f.read())
f.close()

f=open('free.txt','r')
free=eval(f.read())
f.close()

username=input('请输入您需要解冻的帐户名：')
database[username]=free.pop(username)

f=open('database.txt','w')
f.write(str(database))
f.close()
print('帐户名%s已经解冻，可以正常登录了'%username)