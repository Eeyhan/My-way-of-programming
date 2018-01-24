#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/19 0019 21:43

import os,sys

base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_dir)

from libs import auth
from libs import logger
from libs import transaction
from libs import accounts
from conf import settings


# 用户数据，作为标志位以及缓存用户信用卡信息
account_data = {
    'account_id':None,
    'is_auth':False,
    'data':None
}



# 用户日志
account_log = logger.logger('account')

# 交易日志
transaction_log = logger.logger('transaction')

# 账户信息
def userinfo(data):
    '''
    print user of data
    :param data: user data
    :return:
    '''
    for k,v in data.items():
        print(k,':',v)

# 查询账单
def select(data):
    '''
    check transaction data
    :param data: user data
    :return:
    '''
    check_path = '%s/log/transaction.log'%settings.BASE_DIR
    with open(check_path) as f:
        for i in f.readlines():
            if str(data['id']) in i:
                print(i)

# 退出
def logout(data):
    '''
    quit the programs func
    :param data: user data
    :return:
    '''
    print('account [%s] quit...'%data['id'])
    exit()

# 还款
def repay(data):
    '''
    user repay bill
    :param data: user data
    :return:
    '''
    corrent_accdata = accounts.corrent_accdata(data['id'])

    print('''---------- user %s bill ----------
    creadit:    %s
    balance:    %s
    '''%(data['id'],data['credit'],data['balance']))

    back_flag = False
    while  not back_flag:
        repay_amount = input("\033[36;1mplease enter amount or 'b' to back:\033[0m").strip()

        if repay_amount == 'b':
            back_flag = True

        print() #此处的打印空是为了换行美观，否则日志输出会和repay_amount在同一行
        if len(repay_amount) > 0 and repay_amount.isdigit():
            new_data = transaction.change(data,repay_amount,transaction_log,'repay')
            if new_data:
                print('\033[46;1mnew balance:[%s]\033[0m'%new_data['balance'])
        else:
            print('\033[31;1m[%s] not integer,only support integer\033[0m'%repay_amount)

        if repay_amount == 'b':
            back_flag = True

# 取款
def draw(data):
    '''
    user repay bill
    :param data: user data
    :return:
    '''
    corrent_accdata = accounts.corrent_accdata(data['id'])

    print('''---------- user %s bill ----------
    creadit:    %s
    balance:    %s
    '''%(corrent_accdata['id'],corrent_accdata['credit'],corrent_accdata['balance']))

    back_flag = False
    while  not back_flag:
        draw_amount = input("\033[36;1mplease enter amount or 'b' to back:\033[0m").strip()

        if draw_amount == 'b':
            back_flag = True

        if len(draw_amount) > 0 and draw_amount.isdigit():
            new_data = transaction.change(corrent_accdata,draw_amount,transaction_log,'draw')
            if new_data:
                print('\033[46;1mnew balance:[%s]\033[0m'%new_data['balance'])
        else:
            print('\033[31;1m[%s] not integer,only support integer\033[0m'%draw_amount)

# 转账
def transfer(data):
    '''
    user1 transfer money to user2
    :param data: user data
    :return:
    '''
    corrent_accdata = accounts.corrent_accdata(data['id'])

    print('''---------- user %s bill ----------
    creadit:    %s
    balance:    %s
    '''%(corrent_accdata['id'],corrent_accdata['credit'],corrent_accdata['balance']))

    back_flag = False
    while  not back_flag:
        transfer_amount = input("\033[36;1mplease enter amount or 'b' to back:\033[0m").strip()

        if transfer_amount == 'b':
            back_flag = True

        if len(transfer_amount) > 0 and transfer_amount.isdigit():
            transfer_user_id = input("\033[36;1mplease enter user id :\033[0m").strip()
            try:
                transfer_userdata = accounts.corrent_accdata(transfer_user_id)
                new_data = transaction.change(corrent_accdata,transfer_amount,transaction_log,'transfer')
                if new_data:
                    transfer_userdata['balance'] += float(transfer_amount)
                    accounts.dump_accdata(transfer_userdata)
                    print('\033[46;1mtrade successfully!\033[0m')
                    print('\033[46;1mnew balance:[%s]\033[0m'%new_data['balance'])
            except Exception as reason:
                    print('\033[31;1mtransaction failure!\033[0m')
                    print(reason)
        else:
            print('\033[31;1m[%s] not integer,only support integer\033[0m'%transfer_amount)


# 信用卡操作对象
def optionlist(data):
    '''

    :param data: user's data
    :return:
    '''
    menu = u'''\033[32;1m
    1.账户信息
    2.还款
    3.取款
    4.转账
    5.查询账单
    6.退出\033[0m'''
    option_dict = {
        '1':userinfo,
        '2':repay,
        '3':draw,
        '4':transfer,
        '5':select,
        '6':logout
    }
    exit_flag = False
    while  not exit_flag:
        print(menu)
        user_option  = input('\033[36;1mplease enter the option number:\033[32;1m')
        if user_option in option_dict:
            option_dict[user_option](data)
        else:
            print("\033[31;1m sorry,haven't option [%s]\033[0m"%user_option)

# 运行
def run():
    '''
    运行函数，将整个项目运行起来
    :return:
    '''
    userdata = auth.login(account_data,account_log)
    if account_data['is_auth'] == True:
        account_data['data'] = userdata
        optionlist(userdata)