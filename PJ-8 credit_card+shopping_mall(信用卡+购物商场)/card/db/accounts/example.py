#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/20 0020 15:43

import json,sys,os,datetime

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(base_dir)

from conf import settings
from libs import db

path = db.db(settings.DATABASEINFO)

acc_dic = {
    'id': 123, #卡号
    'password': 'abc', #密码
    'credit': 15000, #额度
    'balance': 15000, #余额
    'enroll_date': '2016-01-02', #注册日期
    'expire_date': '2021-01-01', #失效日期
    'pay_day': 22, #还款日
    'status': 0 # 0 = normal, 1 = locked, 2 = disabled
}

id = int(input('\033[36;1menter your user id:\033[0m'))
corrent_path = '%s/%s.json'%(path,id)

acc_dic['id'] = id

enroll_date = datetime.date.today()
expire_date = enroll_date + datetime.timedelta(days=365*5)

acc_dic['enroll_date'] = str(enroll_date)
acc_dic['expire_date'] = str(expire_date)

with open(corrent_path,'w') as f:
    json.dump(acc_dic,f)





