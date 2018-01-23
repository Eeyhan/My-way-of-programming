#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/19 0019 21:41

import os,sys

base_dir = os.path.dirname(os.path.dirname(__file__))

sys.path.append(base_dir)


from libs import main

if __name__ == '__main__':
    main.run()

