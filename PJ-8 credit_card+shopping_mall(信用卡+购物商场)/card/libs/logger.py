#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/19 0019 21:54

import logging
from conf import settings

def logger(log_type):

    # 创建一个文件型日志对象
    log_file = '%s/log/%s'%(settings.BASE_DIR,settings.LOG_TYPE[log_type])
    fh = logging.FileHandler(log_file)
    fh.setLevel(settings.LOG_LEVEL)

    # 创建一个输出到屏幕型日志对象
    sh = logging.StreamHandler()
    sh.setLevel(settings.LOG_LEVEL)

    # 设置日志格式
    formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 添加格式到文件型和输出型日志对象中
    fh.setFormatter(formater)
    sh.setFormatter(formater)

    # 创建log对象，命名
    logger = logging.getLogger(log_type)
    logger.setLevel(settings.LOG_LEVEL)

    # 把文件型日志和输出型日志对象添加进logger
    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger