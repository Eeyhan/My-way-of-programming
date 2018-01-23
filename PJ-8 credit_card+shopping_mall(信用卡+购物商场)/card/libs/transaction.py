#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/20 0020 17:50

from conf import settings
from libs import accounts


def change(account_data,amount,logobj,trantype):
    '''
    :param account_data: user data
    :param amount: user entered amount
    :param logobj: transaction logging object
    :param trantype: transaction type
    :return:
    '''
    amount = float(amount)
    if trantype in settings.TRAN_TYPE:
        interest = amount * settings.TRAN_TYPE[trantype]['interest'] #利息
        old_balance = account_data['balance']

        if settings.TRAN_TYPE[trantype]['action'] == 'plus':
            new_balance = old_balance + amount +interest

        elif settings.TRAN_TYPE[trantype]['action'] == 'minus':

            new_balance = old_balance - amount - interest
            if new_balance < 0:
                print("\033[31;1maccount [%s] balance is not sufficient to pay [%s]!\033[0m"
                      %(account_data['id'],amount +interest))
                return

        account_data['balance'] = new_balance
        accounts.dump_accdata(account_data)

        logobj.info('account:%s - transaction:%s - amount:%s - interest:%s'
                    %(account_data['id'],trantype,amount,interest))
        return account_data
    else:
        print('\033[31;1mTransaction type [%s] is not exist!\033[0m'%trantype)



