#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2017/12/5 0005 18:00

from collections import Counter
import copy
'使用字典'

# 商品可以随时上新，也可用另一个文本文档存储

shop_dict = {'1':{'iphoneX':6000},'2':{'MAC':9000},'3':{'coffee':50},'4':{'pythonbook':80},'5':{'CD':20}}

myshop_cart = [] #购物车

print('欢迎来到XXX购物平台！\n您看上哪个商品，输入商品对应的【id】即可购买，如果购物结束输入【quit】即可退出')
for i,m in shop_dict.items():
    for j,k in m.items():
        print('商品id：%s\t商品名：%s\t\t商品单价：%s'%(i,j,k))

salary = int(input('请输入您的透支额度：'))
temp = salary #作为缓存总额，用于后面总共消费多少作计算

while True:
    for i,m in shop_dict.items():
        for j,k in m.items():
            print('商品id：%s\t商品名：%s\t\t商品单价：%s'%(i,j,k))
    shopping = input('请输入商品id（退出请输入“quit”）>>>:')
    if shopping in shop_dict.keys():
        if salary < list(shop_dict[shopping].values())[0]:
            print('您的余额不足')
        else:
            salary -= list(shop_dict[shopping].values())[0]
            myshop_cart.append(list(shop_dict[shopping].keys())[0]) #把商品添加至购物车
            print('您已购买商品【%s】，剩余余额：%s\n'%(list(shop_dict[shopping].keys())[0],salary))
            if not salary:
                print('您的余额为0，不能再购买任何东西，程序已退出，欢迎下次光临')
                break
    elif shopping == 'quit': #购买结束，到收银台结账
        print('您一共购买了以下商品：')
        for i,j in dict(Counter(myshop_cart)).items():
            print('商品名：%s\t数量：%s'%(i,j))

        print('您总共消费了%s元，可用余额为%s元'%(temp-salary,salary))
        print('欢迎下次光临！')
        break
    else:
        print('您的输入有误，请查看是否有id为【%s】的商品'%shopping)

#后期可以添加图形化界面，在客户购买商品的时候，可以不定时在客户购物时发布公告宣布上新商品等等



'不用字典'

# product_list = [
#     ('Mac',9000),
#     ('pythonbook',80),
#     ('bickle',1500),
#     ('CD',20),
#     ('iphoneX',6000),
# ]
#
# print('欢迎来到XXX购物平台！\n您看上哪个商品，输入商品对应的【id】即可购买，如果购物结束输入【quit】即可退出')
# salary = int(input('请输入您的透支额度：'))
# temp1 = salary
# myshop_cart1 = []
# while True:
#     for i,j in enumerate(product_list,1):
#         print('商品id：%s\t商品及价格：%s'%(i,j))
#
#     shopping = input('请输入商品id（退出请输入“quit”）>>>:')
#     if shopping.isdigit():
#         shopping=int(shopping)
#         if shopping > 0 and shopping <= len(product_list):
#             if salary < product_list[shopping-1][1]:
#                 print('您的余额不足')
#             else:
#                 salary -= product_list[shopping-1][1]
#                 myshop_cart1.append(product_list[shopping-1][0]) #把商品名添加至购物车
#                 print('您已购买商品【%s】，剩余余额：%s\n'%(product_list[shopping-1][0],salary))
#                 if not salary:
#                     print('您的余额为0，不能再购买任何东西，程序已退出，欢迎下次光临')
#                     break
#     elif shopping == 'quit':
#
#         templist = copy.deepcopy(myshop_cart1)
#         # print(templist)
#
#         #这里是作去重并避免改动原数据，可以直接用set去重
#
#         for i in myshop_cart1:
#             if templist.count(i)>=2:
#                 templist.remove(i)
#
#         print('您一共购买了以下商品：')
#         for i in templist:
#             print('商品：%s\t\t数量：%s'%(i,myshop_cart1.count(i)))
#         print('您总共消费了%s元，可用余额为%s元'%(temp1-salary,salary))
#         print('欢迎下次光临！')
#         break
#     else:
#         print('您的输入有误，请查看是否有id为【%s】的商品'%shopping)
