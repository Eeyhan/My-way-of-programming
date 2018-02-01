#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2018/1/31 0031 15:43

'学生接口，没有任何修改设置权限，只能查看信息'

from libs.main import Course
from libs.main import School
from libs.main import Teacher
from libs.main import Coursetoteacher
from libs.main import Classes
from libs.main import Student

def show_choice():
    print('-------- 查看选项 --------')
    show = '''
        1.查看选项
        2.查看学校
        3.查看老师
        4.查看课程
        5.查看老师授课范围
        6.查看班级
        7.查看成绩
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

def show_score():

    student_list = Student.get_all_list()
    for k,v in enumerate(student_list,1):
        print(k,v)
    inp = int(input('请选择待查询的学生（输入前面的序号即可）：').strip())
    studentobj = student_list[inp - 1] # 拿到学生对象

    print('-------- 课程教师关联列表 --------')
    Coursetoteacher_list = Coursetoteacher.get_all_list()
    for k,v in enumerate(Coursetoteacher_list,1):
        print(k,v)
    inp = int(input('请输入待查看的课程（输入前面的序号）：').strip())
    courseteacherobj = Coursetoteacher_list[inp - 1]
    # 注意这里，一定要把uuid转为字符串
    print(studentobj.score.get(str(courseteacherobj.id)))

def main():
    choice_dict = {
        '1':show_choice,
        '2':show_school,
        '3':show_teacher,
        '4':show_course,
        '5':show_courseteacher,
        '6':show_classes,
        '7':show_score
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