#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/31 0031 15:43

import os,pickle

from libs.main import Course
from libs.main import School
from libs.main import Teacher
from libs.main import Coursetoteacher
from libs.main import Classes
from libs.main import Student
from libs.main import Score

def show_choice():
    print('-------- 查看选项 --------')
    show = '''
        1.查看选项
        2.查看学校
        3.查看老师
        4.查看课程
        5.查看课程与老师的对应关系
        6.查看班级
        7.注册学生
        8.设置学生成绩
        '''
    print(show)

def show_school():
    print('-------- 查看学校 --------')
    school_list = School.get_all_list()
    for i in school_list:
        print(i)

def show_teacher():
    print('-------- 查看老师 --------')
    teacher_list = Teacher.get_all_list()
    for k in teacher_list:
        print(k)

def show_course():
    print('-------- 查看课程 --------')
    course_list = Course.get_all_list()
    for i in course_list:
        print(i)

def show_courseteacher():
    print('-------- 查看教师授课范围 --------')
    Coursetoteacher_list = Coursetoteacher.get_all_list()
    for i in Coursetoteacher_list:
        print(i)

def show_classes():
    print('-------- 查看班级 --------')
    classes_list = Classes.get_all_list()
    for i in classes_list:
        print(i)

def register_student():
    print('-------- 注册学生 --------')
    name = input('学生姓名：').strip()
    age = input('学生年龄：').strip()

    classes_list = Classes.get_all_list()
    for k,v in enumerate(classes_list,1):
        print(k,v)

    for_classes = int(input('待录入的班级id:'))
    classesobj = classes_list[for_classes-1]

    obj = Student(name,age,classesobj)
    obj.save()

def set_student_core():
    # 获取指定的学生对象
    print('-------- 查看学生 --------')
    student_list = Student.get_all_list()
    for k,v in enumerate(student_list,1):
        print(k,v)
    inp = int(input('请选择待操作的学生（输入前面的序号即可）：').strip())
    studentobj = student_list[inp - 1]

    # 获取课程教师关联对象
    print('-------- 查看课程教师关联 --------')
    cou_tea_list = Coursetoteacher.get_all_list()
    for k,v in enumerate(cou_tea_list,1):
        print(k,v)
    inp2 = int(input('请输入待录入的课程：').strip())
    courteaobj = cou_tea_list[inp2 - 1]

    # 设置成绩
    print('-------- 设置成绩 --------')
    score_number = input('请输入成绩：').strip()
    while not score_number.isdigit():
        score_number = input('不合法的数字，请重新输入成绩：').strip()
    else:
        score_number = int(score_number)

        '''注意这里，大坑，搞了两个多小时！！！
        一定要把uuid转为字符串，不然存入的会是一个uuid对象:<libs.identifier.Course_to_teacherid object at 0x0000000002A76D68>，
        和获取成绩的时候传入的id永远不能匹配，一个是id,一个是对象
        也就永远获取不到'''

        # pickle.dump也要把uuid转为字符串才可以dump
        studentobj.score.set(str(courteaobj.id),score_number)
        path = os.path.join(Student.db_path,str(studentobj.id))
        with open(path,'wb') as f:
            pickle.dump(studentobj,f)


def main():
    choice_dict = {
        '1':show_choice,
        '2':show_school,
        '3':show_teacher,
        '4':show_course,
        '5':show_courseteacher,
        '6':show_classes,
        '7':register_student,
        '8':set_student_core
    }
    show_choice()

    while True:
        inp = input('请输入选项(输入“q”可退出程序):').strip()
        if inp == 'q':
            print('已退出！')
            exit()
        if inp not in choice_dict:
            print('操作异常，没有此选项！\n')
            continue
        func = choice_dict[inp]
        if func() != None:
            print('操作异常！请重新操作！\n')
            return
        print('--------------------------')

if __name__ == '__main__':
    main()