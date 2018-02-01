#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/31 0031 15:41

import os

from libs.main import School
from libs.main import Teacher
from libs.main import Coursetoteacher
from libs.main import Course
from libs.main import Classes


def show_choice():
    print('-------- 查看选项 --------')
    show = '''
        1.查看选项
        2.创建学校
        3.查看学校
        4.创建老师
        5.创建课程
        6.查看课程
        7.创建课程与老师的对应关系
        8.创建班级
        '''
    print(show)

def create_school():
    '''
    创建学校
    :return:
    '''
    print('-------- 创建学校 --------')
    name = input('请输入学校名称：').strip()
    obj = School(name)
    obj.save()

def show_school():
    print('-------- 查看学校 --------')
    school_list = School.get_all_list()
    for i in school_list:
        print(i)

def create_teacher():
    print('-------- 创建老师 --------')
    name = input('请输入老师名称：').strip()
    level = input('请输入老师等级：').strip()
    obj = Teacher(name,level)
    obj.save()

def create_course():
    print('-------- 创建课程 --------')
    school_list = School.get_all_list()
    for k,v in enumerate(school_list,1):
        print(k,v)
    sch = int(input('请选择所属学校(输入前面的序号即可)：').strip())
    schoolobj = school_list[sch - 1]

    name = input('请输入课程名称：').strip()
    price = input('请输入课程价格：').strip()
    period = input('请输入课程周期：').strip()

    obj = Course(name,price,period,schoolobj.id)
    obj.save()
    print('课程 【%s】 创建成功！'%name)

def show_course():
    print('-------- 查看课程 --------')
    course_list = Course.get_all_list()
    for i in course_list:
        print(i)


def create_course_teacher():
    '''
    为课程分配老师
    :return:
    '''
    print('-------- 查看课程 --------')
    course_list = Course.get_all_list()
    for k,v in enumerate(course_list,1):
        print(k,v)
    cour_id = int(input('请选择入学课程（输入序号即可）：').strip())
    courseobj = course_list[cour_id - 1]

    print('-------- 查看老师 --------')
    teacher_list = Teacher.get_all_list()
    for k,v in enumerate(teacher_list,1):
        print(k,v)
    teac_id = int(input('请选择授课老师（输入序号即可）：').strip())
    teacherobj = teacher_list[teac_id - 1]

    obj = Coursetoteacher(courseobj.id,teacherobj.id)
    obj.save()


def create_classes():

    print('-------- 创建班级 --------')
    name = input('请输入班级名称：').strip()
    tuition = input('请输入学费：')

    school_list = School.get_all_list()
    for k,v in enumerate(school_list,1):
        print(k,v)
    sch = int(input('请选择学校(输入前面的序号即可)：').strip())
    schoolobj = school_list[sch - 1]

    courseteacher_list = Coursetoteacher.get_all_list()
    for k,v in enumerate(courseteacher_list,1):
        print(k,v)
    courteac_id = int(input('请选择课程教师关联（输入序号即可）：').strip())
    coursetteacherobj = courseteacher_list[courteac_id - 1]

    obj = Classes(name,tuition,schoolobj.id,coursetteacherobj)
    obj.save()


def  main():
    choice_dict = {
        '1':show_choice,
        '2':create_school,
        '3':show_school,
        '4':create_teacher,
        '5':create_course,
        '6':show_course,
        '7':create_course_teacher,
        '8':create_classes,
    }
    show_choice()
    while True:
        inp = input('请输入选项(输入“q”可退出程序):').strip()
        if inp == 'q':
            print('已退出！')
            exit()
        if inp not in choice_dict:
            print('选项错误，请重新选择')
            continue
        func = choice_dict[inp]
        if  func() != None:
            print('操作异常，请重新操作！\n')
            return
        print('--------------------------')

if __name__ == '__main__':
    main()