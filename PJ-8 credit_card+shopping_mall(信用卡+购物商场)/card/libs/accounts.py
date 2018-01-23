#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/20 0020 22:38


from conf import settings
from libs import db
import json

def corrent_accdata(userid):
    '''

    :param userid: user  card's id
    :return:
    '''
    accdata_path = db.db(settings.DATABASEINFO)
    acc_file = '%s/%s.json'%(accdata_path,userid)
    with open(acc_file) as f:
        corrent_accdata = json.load(f)
        return corrent_accdata

def dump_accdata(data):
    '''

    :param data: user data
    :return:
    '''
    accdata_path = db.db(settings.DATABASEINFO)
    acc_file = '%s/%s.json'%(accdata_path,data['id'])
    with open(acc_file,'w') as f:
        json.dump(data,f)

    return True