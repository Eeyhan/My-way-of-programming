 #!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/21 0024 17:44

import sys,json,os
from collections import Counter

base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_dir)

from card.conf import settings
from card.libs import db


# 载入商城账号信息，商城和信用卡并不是等同的
user_path = '%s/mall/yang.json'%base_dir
with open(user_path) as f:
    userdata = json.load(f)

# 读取信用卡
path = db.db(settings.DATABASEINFO)
account_path = '%s/%s.json'%(path,userdata['id'])
with open(account_path) as f:
    accountdata = json.load(f)

# 账户可用余额
salary = accountdata['balance']
#缓存总额，用于后面总共消费多少作计算
temp = salary
#购物车
cart = []

#商品总清单
product ={
    '手机':{
        '1':{'IphoneX':8388.00},
        '2':{'Iphone8':5088.00},
        '3':{'一加5T':3270.00},
        '4':{'魅族pro7':1999.00},
        '5':{'小米MIX2':3299.00},
        '6':{'华为p10':3488.00}
    },
    '电脑':{
        '7':{'联想R720-15I':7399.00},
        '8':{'惠普战66ProG1':6499.00},
        '9':{'戴尔XPS13':6299.00},
        '10':{'MacBookAir':6988.00}
    },
    '日用品':{
        '11':{'高露洁牙刷':12.90},
        '12':{'三利纯棉浴巾':32.50},
        '13':{'半球电水壶':49.00}
    }
}

login_status = False  #登录状态标志位

#登录验证
def login(func):
    def inner():
        global login_status
        while not login_status:
            print('\033[32;1m请登录\033[0m')
            username = input('\033[32;1musername:\033[0m')
            password = input('\033[32;1mpassword:\033[0m')
            while username not in userdata or password != userdata[username]:
                print('\033[31;1m用户名或密码错误,请重新登录\033[0m')
                username = input('\033[32;1musername:\033[0m')
                password = input('\033[32;1mpassword:\033[0m')
            else:
                print('\033[34;1m登录成功!\n')
                login_status = True
                return func()
        else: #已登录状态
            return func()
    return inner

#手机页面
@login
def phone(string='手机'):
    shopping_cart(string)

#电脑页面
@login
def pc(string='电脑'):
    shopping_cart(string)

#日用品页面
@login
def life(string='日用品'):
    shopping_cart(string)

#主页
@login
def home():
    print('\033[36;1m首页，js动态切换图片；精品促销；XX品牌日\033[0m')

#消费流水
@login
def consume():
    consume = temp-salary #消费金额
    if consume > 0:
        print('\033[36;1m您当前的消费流水详细账单：\033[0m')
        for i,j in dict(Counter(cart)).items():
            print('\033[36;1m%s 数量：%s\033[0m'%(i,j))
        print('\033[46;1m您总共消费了 %.2f 元，可用余额为 %.2f 元\033[0m\n'%(temp-salary,salary))
    else:
        print('\033[31;1m您还未购买任何物品\033[0m\n')

# 更新用户数据
def dump():
    global account_path,accountdata
    accountdata['balance'] = salary
    with open(account_path,'w') as f:
        json.dump(accountdata,f)
    return accountdata

# 退出
def logout():
    acc = dump()
    if acc:
        print('\033[36;1m欢迎下次光临！您已退出!\033[0m')
        exit()

#购物车
def shopping_cart(string):
    global salary
    for page,goods_msg in product.items():
        if page == string:
            while True:
                print('\033[36;1m页面：%s\033[0m\n'%page)
                for ID,goods in goods_msg.items():
                    for name,price in goods.items():
                        print('\033[32;1m商品id：%s\t\t\t商品名：%s\t\t\t价格：%s\033[0m'%(ID,name,price))
                shopping = input('\033[32;1m请输入商品id（需要返回上一级菜单请输入“b”）>>>:\033[0m')
                if shopping in goods_msg.keys():
                    gname = list(goods_msg[shopping].keys())[0]
                    gprice =list(goods_msg[shopping].values())[0]
                    if salary < gprice:
                        print('\033[31;1m您的余额不足\033[0m')
                    else:
                        salary -= gprice
                        print('\033[46;1m您已购买商品 %s -- 单价 %.2f，剩余余额：%.2f\033[0m\n'%(gname,gprice,salary))
                        cart.append('\033[32;1m商品:%s 单价:%.2f\033[0m'%(gname,gprice))
                        if not salary: #购买后再次检测信用卡剩余额度
                            print('\033[31;1m您的余额为0，不能再购买任何东西，程序已退出，欢迎下次光临\033[0m')
                            break
                elif shopping == 'b': #购买结束，到收银台结账
                    print('\033[32;1m已返回上一级\033[0m\n')
                    break
                else:
                    print('\033[31;1m您的输入有误，请查看是否有id为【%s】的商品\033[0m'%shopping)

#主函数
def man():
    mapper = {'1':home,'2':pc,'3':phone,'4':life,'5':consume,'6':logout} #映射函数
    print('\033[32;1m-------欢迎光临XXX商城-------\033[0m')
    while True:
        print('\033[32;1m1.主页\n2.电脑\n3.手机\n4.日用品\n5.打印流水凭条\n6.退出\033[0m')
        page = input('\033[32;1m请选择访问页面（输入前面的序号即可）：\033[0m')
        if page in mapper:
            mapper[page]()
        else:
            print('\033[31;1m输入有误！！\033[0m')

if __name__ == '__main__':
    man()


