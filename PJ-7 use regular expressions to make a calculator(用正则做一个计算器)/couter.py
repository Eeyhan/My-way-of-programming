#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2017/12/23 0023 21:31

import re

def format_string(string): #格式化字符串，把符号格式化
    string = string.replace('++','+')
    string = string.replace('-+','-')
    string = string.replace('--','+')
    string = string.replace('*+','*')
    string = string.replace('/+','/')
    string = string.replace(' ','')
    return string

def counter_md(string): #乘除
    pattern_str2 = '\d+\.?\d*[*/][+\-]?\d+\.?\d*' #匹配乘除法，带上正负号,[]中的 - 有特殊意义，所以要转义

    while re.findall(pattern_str2,string):
        expression = re.search(pattern_str2,string).group()

        #如果有乘法，分割并分别运算
        if expression.count('*'):
            x,y = expression.split('*')
            mul_result = str(float(x)*float(y))
            string = string.replace(expression,mul_result)
            string = format_string(string)
        #如果有除法，分割并分别运算
        if expression.count('/'):
            x,y = expression.split('/')
            div_result = str(float(x)/float(y))
            string = string.replace(expression,div_result)
            string = format_string(string)
    return string

def counter_as(string): #加减
    pattern_add = '[\-]?\d+\.?\d*\+[+\-]?\d+\.?\d*' #匹配加法
    pattern_sub = '[\-]?\d+\.?\d*\-[+\-]?\d+\.?\d*' #匹配减法
    #处理加法
    while re.findall(pattern_add,string):
        add_list = re.findall(pattern_add,string) #将结果分割成一个小式子
        for add_str in add_list:  #迭代每个小式子，分别计算
            x,y = add_str.split('+')
            add_result = '+'+str(float(x)+float(y))
            string = string.replace(add_str,add_result) #得到的结果替换到式子中
    #处理减法
    while re.findall(pattern_sub,string):
        sub_list = re.findall(pattern_sub,string)
        for sub_str in sub_list:
            numbers = sub_str.split('-')
            #如果分割出来的小式子里有如-5-3的式子，会分割出['','5','3']则再分割一次
            if len(numbers) == 3:
                result = 0 #定义变量，方便后续存储结果
                for v in numbers:
                    if v:
                        result -= float(v)
            else: #正常结果，比如4-5，分割得到的则是['4','5']
                x,y = numbers
                result = float(x) - float(y)
            #替换字符串
            string = string.replace(sub_str,str(result))

    return string

def check(string): #检查合法性
    check_flag = True #标志位
    if not string.count('(') == string.count(')'):
        print('括号数量不统一')
        check_flag = False
    if re.findall('[a-zA-Z]+',string):
        check_flag = False
        print('非法字符')
        check_flag = False
    return check_flag

if __name__ == '__main__':
    #info = '20-4+9*((44-22+134/3 - (-3+33+34*5/2*5-9/3*55)-45-3)+55+3*234)'
    # 检验合法性
    info = input('请输入式子：')
    if check(info):
        print('info:',info)
        info = format_string(info)
        print(info)
        print('eval(info):',eval(info)) #作为与输出结果对比的验证
        while info.count('(') > 0:  #计算括号内的式子
            pattern_str = re.search('\([^()]*\)',info).group()
            #按照运算优先级，先计算乘除法的结果
            md_result = counter_md(pattern_str)
            #再计算加减法的结果
            as_result = counter_as(md_result)
            #把计算得到的结果作[1:-1]切片，把括号去掉再重新格式化替换原数据替换到式子中
            info = format_string(info.replace(pattern_str,as_result[1:-1]))
        else: #计算括号外的式子，不用再匹配直接运算
            md_result = counter_md(info)
            as_result = counter_as(md_result)
            info = info.replace(info,as_result)
        print('the result is :',info.replace('+',''))