#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan
import os,sys
server_base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(server_base_path)

from lib import servers

def start():
    servers.Server().run_always()

if __name__ == '__main__':
    start()