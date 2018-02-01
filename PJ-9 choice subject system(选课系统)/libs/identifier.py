#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/31 0031 15:44

import os,pickle
from libs import common

class Id():
    def __init__(self,role,db_path):
        role_list = [
            'admin','school','course','student','course_to_teacher','teacher','classes'
        ]
        if role not in role_list:
            raise Exception('用户角色定义错误，正确选项应为：%s'%'|'.join(role_list))

        self.role = role
        self.id = common.create_uuid()
        self.db_path = db_path

    def __str__(self):
        return self.id

    def get_obj_by_uuid(self):
        for name in os.listdir(os.path.join(self.db_path)):
            if name == self.id:
                return pickle.load(open(os.path.join(self.db_path,self.id),'rb'))

class Adminid(Id):
    def __init__(self,db_path):
        super().__init__('admin',db_path)

class Teacherid(Id):
    def __init__(self,db_path):
        super().__init__('teacher',db_path)

class Schoolid(Id):
    def __init__(self,db_path):
        super().__init__('school',db_path)

class Courseid(Id):
    def __init__(self,db_path):
        super().__init__('course',db_path)

class Studentid(Id):
    def __init__(self,db_path):
        super().__init__('student',db_path)

class Course_to_teacherid(Id):
    def __init__(self,db_path):
        super().__init__('course_to_teacher',db_path)

class Classes(Id):
    def __init__(self,db_path):
        super().__init__('classes',db_path)


