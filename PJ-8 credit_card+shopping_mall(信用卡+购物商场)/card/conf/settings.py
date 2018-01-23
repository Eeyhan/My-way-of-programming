#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/19 0019 21:56

import os,sys,logging

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 设置日志等级
LOG_LEVEL = logging.INFO

# 存储日志类型
LOG_TYPE = {
    'transaction':'transaction.log',
    'account':'account.log'

}

# 数据库信息
DATABASEINFO = {
    'engine':'file',# 数据库类型，可以为文件，可以为数据库
    'dirname':'accounts',# 数据文件目录名
    'path':'%s/db'%BASE_DIR
}

# 交易类型
TRAN_TYPE = {
    'repay':{'action':'plus','interest':0},
    'draw':{'action':'minus','interest':0.05},
    'transfer':{'action':'minus','interest':0.05}
}