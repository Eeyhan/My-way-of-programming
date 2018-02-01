#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/31 0031 16:58

import os,time,pickle
from libs import identifier
from config import settings

class Base:
    def save(self):
        '''
        用pickle将用户对象保存到文件
        :return:
        '''
        id = str(self.id)
        file_path = os.path.join(self.db_path,id)
        pickle._dump(self,open(file_path,'wb'))

class Admin(Base):
    db_path = settings.admin_dbpath
    def __init__(self,username,password):
        '''

        :param username:
        :param pasword:
        :return:
        '''
        self.id = identifier.Adminid(Admin.db_path)
        self.username = username
        self.password = password
        self.create_time = time.strftime("%Y-%m-%d")

    @staticmethod
    def login(user,pwd):
        '''

        :param user:

        :param pwd:
        :return:
        '''

        for i in  os.listdir(Admin.db_path):
            adminobj = pickle.load(os.path.join(Admin.db_path,i))
            if user == adminobj.name and pwd == adminobj.password:
                return adminobj


class School(Base):
    db_path = settings.school_dbpath

    def __init__(self,name):
        self.id = identifier.Schoolid(School.db_path)
        self.schoolname = name
        self.income = 0 #学校收入

    def __str__(self):
        return self.schoolname

    @staticmethod
    def get_all_list():
        objlist = []
        for i in os.listdir(School.db_path):
            obj = pickle.load(open(os.path.join(School.db_path,i),'rb'))
            objlist.append(obj)
        return objlist

class Teacher(Base):
    db_path = settings.teacher_dbpath

    def __init__(self,name,level):
        self.id = identifier.Teacherid(Teacher.db_path)
        self.teachername = name
        self.teacherlevel = level
        self.__account = 0 #老师收入

    def __str__(self):
        return '教师姓名：%s -- 教师等级：%s'%(self.teachername,self.teacherlevel)
    @staticmethod
    def get_all_list():
        objlist = []
        for i in os.listdir(Teacher.db_path):
            obj = pickle.load(open(os.path.join(Teacher.db_path,i),'rb'))
            objlist.append(obj)
        return objlist

    @staticmethod
    def register():
        pass

class Course(Base):
    db_path = settings.course_dbpath

    def __init__(self,name,price,period,school_id):
        '''

        :param name:
        :param price:
        :param period:
        :param school_id: 学校id,相当于学校对象
        :return:
        '''
        self.id = identifier.Courseid(Course.db_path)
        self.coursename = name
        self.courseprice = price
        self.courseperiod = period
        self.schoolid = school_id

    def __str__(self):
        return '课程名：%s；课程价格：%s；课程周期：%s；所属学校：%s'%(
            self.coursename,self.courseprice,self.courseperiod,self.schoolid.get_obj_by_uuid().schoolname)

    @staticmethod
    def get_all_list():
        objlist = []
        for i in os.listdir(Course.db_path):
            obj = pickle.load(open(os.path.join(Course.db_path,i),'rb'))
            objlist.append(obj)
        return objlist

class Coursetoteacher(Base):
    db_path = settings.course_to_teacehr_dbpath

    def __init__(self,course_id,teacher_id):
        self.id = identifier.Course_to_teacherid(Coursetoteacher.db_path)
        self.courseid = course_id
        self.teacherid = teacher_id

    def __str__(self):
        return '课程：%s -- 授课老师：%s'%(self.courseid.get_obj_by_uuid().coursename,self.teacherid.get_obj_by_uuid().teachername)

    @staticmethod
    def get_all_list():
        objlist = []
        for i in os.listdir(Coursetoteacher.db_path):
            obj = pickle.load(open(os.path.join(Coursetoteacher.db_path,i),'rb'))
            objlist.append(obj)
        return objlist

class Classes(Base):
    db_path = settings.classes_dbpath

    def __init__(self,name,tuition,school_id,course_to_teacher_list):
        '''

        :param name:
        :param tuition: 学费
        :param school_id: 学校id
        :param course_to_teacher_list: Coursetoteacher对象列表
        :return:
        '''
        self.id = identifier.Classes(Classes.db_path)
        self.name = name
        self.tuition = tuition #学费
        self.schoolid = school_id
        self.coursetoteacherlist = course_to_teacher_list

    def __str__(self):
        return '班级名：%s -- 学费：%s'%(self.name,self.tuition)

    @staticmethod
    def get_all_list():
        objlist = []
        for i in os.listdir(Classes.db_path):
            obj = pickle.load(open(os.path.join(Classes.db_path,i),'rb'))
            objlist.append(obj)
        return objlist

class Score:
    '''
    成绩
    '''
    def __init__(self,student_id):
        self.studentid = student_id
        self.score_dict = {}

    def set(self,coure_to_teacher_id,number):
        self.score_dict[coure_to_teacher_id] = number

    def get(self,course_to_teacher_id):
        return self.score_dict.get(course_to_teacher_id,None)

class Student(Base):
    db_path = settings.student_dbpath

    def __init__(self,name,age,classes_id):
        self.id = identifier.Studentid(Student.db_path)
        self.studentname = name
        self.age = age
        self.classesid = classes_id
        self.score = Score(self.id) #成绩

    def __str__(self):
        return '学生姓名：%s -- 学号：%s'%(self.studentname,self.id)

    @staticmethod
    def register():
        pass

    @staticmethod
    def get_all_list():
        objlist = []
        for i in os.listdir(Student.db_path):
            obj = pickle.load(open(os.path.join(Student.db_path,i),'rb'))
            objlist.append(obj)
        return objlist