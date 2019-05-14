#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:yavan
import os,sys
base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)

from server.lib import client

def run_client():
    client.Client().run()
if __name__ == '__main__':
    run_client()