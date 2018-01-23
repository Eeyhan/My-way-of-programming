#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/19 0019 21:53

import json,os,time
from conf import settings
from libs import db

def auth(userid,password):
    '''
    account libs func
    :param userid: user card id
    :param password: user pasword
    :return:
    '''
    userdbpath = db.db(settings.DATABASEINFO)
    account_file = '%s/%s.json'%(userdbpath,userid)
    # print(account_file)
    if os.path.isfile(account_file):
        with open(account_file) as f:
            account_data = json.load(f)
            if account_data['password'] == password:
                indate = time.mktime(time.strptime(account_data['expire_date'],'%Y-%m-%d'))
                if indate < time.time():
                    print("\033[31;1m your card was out of date\033[0m")
                else:
                    return account_data
            else:
                print('\033[31;1m your id or password incorrect\033[0m')
    else:
        print('\033[31;1maccount [%s] does not exist\033[0m'%userid)


def login(data,logobj):
    '''
    account login func
    :param data: user's data
    :param logobj: account logger object
    :return:
    '''
    count = 0
    while data['is_auth'] is not True and count < 3:
        userid = input("\033[36;1mplease enter your card's id:\033[0m").strip()
        password = input('\033[36;1menter your password:\033[0m').strip()
        userauth = auth(userid,password)
        if userauth:
            data['is_auth'] = True
            data['account_id'] = userid
            return userauth
        count +=1

    else:
        logobj.error('\033[31;1maccount [%s] too many login attempts\033[0m' % userid)
        exit()
