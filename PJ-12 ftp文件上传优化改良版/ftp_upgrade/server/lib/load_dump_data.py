#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan

import os,sys,json

from conf import settings

def load_data():
    '''
    加载用户数据
    :return:
    '''

    with open(os.path.join(settings.data_path,'.userdata')) as f:
        userdata = json.load(f)
    return userdata

def dump_data(userdata):
    # username = list(userdata.keys())[0]
    # with open(os.path.join())
    pass