#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2017/12/9 0009 13:16

f=open('chinamap.txt','r')
china_map_dict = eval(f.read())
f.close()

current_leval = china_map_dict #实现动态循环
parent_list = [] #把所有列表父级放进列表
while True:
    for key in current_leval:
        print(key)
    choice = input('>>>：').strip()
    if len(choice) == 0:continue
    if choice in current_leval:
        temp = input('发现以上数据【%s】有错？你想修改或者删除【%s】吗？【yes/no】>>>:'%(choice,choice))
        while True:
            if temp == 'yes':
                temp = input('您是修改还是删除？【revise/delete】>>>:')
                if temp == 'revise':
                    value = input('请输入您的正确值：')
                    current_leval[value] = current_leval.pop(choice)
                    print('已修改')
                    break
                elif temp == 'delete':
                    current_leval.pop(choice)
                    print('已删除',end='') #为了和后面的异常放在一行组合为一句
                    break
                else:
                    print('输入有误！已自动进入下一级，需要修改请回退到上一级')
                    break
            elif temp == 'no':break
            else:
                print('输入有误！已自动进入下一级，需要修改请回退到上一级')
                break
        try:
            parent_list.append(current_leval)
            current_leval = current_leval[choice] #进入子级
        except KeyError as reson:
            print(reson)
    elif choice == 'back':
        if parent_list:
            current_leval=parent_list.pop() #取出父级（上一级）
    elif choice == 'quit':
        print('程序已退出')
        break
    else:
        while True:
            temp = input('无选项【%s】,你想添加此项吗？【yes/no】>>>:'%choice)
            if temp == 'yes':
                value = input('请输入您为【%s】添加的数据（可以为空）>>>:'%choice).strip()
                current_leval[choice] = {value:{}}
                break
            elif temp == 'no':break
            else:
                print('输入有误！！')
                break
f=open('chinamap.txt','w')
f.write(str(china_map_dict))
f.close()




