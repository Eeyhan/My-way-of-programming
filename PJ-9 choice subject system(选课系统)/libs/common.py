#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/31 0031 15:33

'创建id'

import hashlib,uuid,time

def create_uuid():
    return str(uuid.uuid1())


def create_md5():
    m = hashlib.md5()
    m.update(bytes(str(time.time()),encoding='utf8'))
    return m.hexdigest()
