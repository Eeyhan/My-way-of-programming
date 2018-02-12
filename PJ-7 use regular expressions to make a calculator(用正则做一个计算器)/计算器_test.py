#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2017/12/23 0021 20:55

import re


def check(string): #检查合法性
    flag = True
    if re.search('[a-zA-Z]',string):
        flag = False
    return flag

def Format(string): #格式化
    string = string.replace('+-','-').replace('-+','-')
    string = string.replace('++','').replace('--','')
    string = string.replace('(','').replace(')','')
    return string

def couter(string): #计算
    pattern_md = '\d+\.?\d*([*/]\d+\.?\d*)+' #如果下面用findall的话改成 '\d+\.?\d*(?:[*/]\d+\.?\d*)+'
    pattern_as = '\d+\.?\d*([+\-]\d+\.?\d*)+'

    def mul_div(string):
        while re.search(pattern_as,string):
            expression = re.search(pattern_as,string).group()

    add_sub = re.search('',string)
    if add_sub:
        re.split(add_sub,'[+-]')
        mul_div = re.search('\d+\.?\d*[/*]\d+\.?\d',string)

def man(string): #主函数
    if check(string):
        while re.search(r'\([^()]+\)',string).group():
            temp = re.search(r'\([^()]+\)',string).group()
            string_in = Format(string)
            result = couter(string_in)
            string = string.replace(temp,str(result))
    else:
        print('计算中不能带有除数字和算术符号以外的其他字符')

    return string

if __name__ == '__main__':
    info = '1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )'
    print(man(info))