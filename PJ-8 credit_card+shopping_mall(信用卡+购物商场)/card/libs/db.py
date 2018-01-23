#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/19 0019 22:51


def fl_db(parms):
    '''

    :param parms: malldb type
    :return: malldb path
    '''
    # print('file malldb:,parms')
    db_path = '%s/%s'%(parms['path'],parms['dirname'])
    # print(db_path)
    return db_path

def ml_db(parms):
    pass

def mo_db(parms):
    pass

def oe_db(parms):
    pass

def db(parms):
    '''

    :param parms: malldb information
    :return:
    '''
    db_dict = {
        'file':fl_db,
        'mysql':ml_db,
        'mongodb':mo_db,
        'orlcle':oe_db,
    }
    if parms['engine'] in db_dict:
        return db_dict[parms['engine']](parms)