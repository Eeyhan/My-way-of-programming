#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/31 0031 15:48

import os,sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.append(BASE_DIR)

admin_dbpath = os.path.join(BASE_DIR,'db','admin')
teacher_dbpath = os.path.join(BASE_DIR,'db','teacher')
student_dbpath = os.path.join(BASE_DIR,'db','student')
school_dbpath = os.path.join(BASE_DIR,'db','school')
course_dbpath = os.path.join(BASE_DIR,'db','course')
course_to_teacehr_dbpath = os.path.join(BASE_DIR,'db','course_to_teacher')
classes_dbpath = os.path.join(BASE_DIR,'db','classes')


