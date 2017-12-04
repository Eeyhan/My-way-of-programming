# -*- coding:utf-8 -*-

#九九乘法表
frist=1
while frist<=9:
    second=1
    while second<=frist:
	    print(str(second)+'*'+str(frist)+'='+str(second*frist),end='\t')
	    second+=1
    print()
    frist+=1
