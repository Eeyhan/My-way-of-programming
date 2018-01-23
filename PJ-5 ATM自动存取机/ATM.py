#!usr/bin/env python
#-*- coding:utf-8 -*-

# author:yangva
# datetime:2017/12/15 0015 13:32

import  random,time
atm_fault = random.randint(0,100) #ATM机随机故障系数
if atm_fault == 0:
    print('ATM出现故障，暂时不可用，抱歉给您带来不便')
else:
    print('ATM播放幻灯片，推销新业务（信用卡办理，VIP会员特权，新卡新功能等等）')
    #插入卡操作
    try:
        #模拟读卡的操作，这里用文本文档代替
        card = open(input('欢迎光临，请在下方插入口插入您的银行卡（输入文本文件路径和文件名）：'))
        print('正在读卡，请稍后。。。')
        time.sleep(2)
        f = eval(card.read())
        username = list(f.keys())[0] #取出账户名
        user_id = f[username]['ID'] #取出银行卡号
    except (NameError,IOError,FileNotFoundError):  #输入的文本不存在则捕获
        print('插入卡操作过程有误，请检查是否存在该文件或打开该文件的权限')
    else:

        f = open('database.txt','r')
        database = eval(f.read())
        f.close()  #这里不用with 语句，为保证数据库文件能立即关闭
        print('%s先生，欢迎您!!!'%username[0]) #问候语
        if username not in database.keys():
            print('您的账户已冻结，请本人携带身份证到银行柜台解冻\n已退卡，请收好您的银行卡')
        else:
            password = input('请输入您的密码(密码为6位数字),请注意周围环境以及遮挡键盘操作：').strip()  #后期可以改为语言提示
            count = 0  #用于操作计数
            ctrl_flag = False #标志位，用于跳出多层循环
            while not ctrl_flag:
                if count == 2:
                    print('您已输入多次错误密码，银行账户已冻结')
                    with open('log.txt','a')  as f2: #写入日志
                        database['freeze'+username] = database.pop(username)
                        f1 = open('database.txt','w')  #同样的，不用with语句，保证数据文件立即关闭
                        f1.write(str(database))
                        f2.write(str(time.strftime("%Y %b %d %X"))+'\n用户 %s 的银行卡已冻结\n'%user_id)
                        f1.close()
                    ctrl_flag = True
                    break
                if len(str(password)) == 6: #用于判断输入的密码位数是否正确
                    if password == database[username]['password']:

                        database_bk = database #做临时备份数据的操作，方便后面出错时会滚
                        temp = '' #凭条
                        while not ctrl_flag:
                            cont = input('1.取款\n2.存款\n3.转账\n4.查询\n5.打印凭条\n6.退卡\n请选择交易类型(输入对应的序号即可):')
                            #账户主体操作
                            if cont == '1': #取款
                                withdraw_money = int(input('请输入取款金额（最低一百）：')) #ATM存取都是100的整数，直接用int类型
                                while withdraw_money %100 != 0:
                                    print('输入金额不是100的整数倍，请重新输入')
                                    withdraw_money = int(input('请输入取款金额（最低一百）：'))
                                else:
                                    if withdraw_money > database[username]['balance']:
                                        print('操作失败，您输入的金额大于您的余额总数')
                                    else:
                                        time.sleep(3)
                                        print('已成功出钞，请取走您的钞票 %s元'%withdraw_money)
                                        database[username]['balance'] -= withdraw_money
                                        with open('log.txt','a') as f:  #写入日志
                                            f.write(str(time.strftime("%Y %b %d %X"))+'\t卡号为 %s 的用户 %s 取出金额：%d\n'%(user_id,username,withdraw_money))
                                        temp += str(time.strftime("%Y %b %d %X"))+'\t取款金额：%d\n'%withdraw_money  #记录凭条

                            elif cont == '2': #存款
                                save_money = int(input('请将钞票叠好，并整齐放入存钞口(输入存款金额,最低一百)：')) #ATM存取款都是100的整数，直接用int类型
                                while save_money %100 != 0:
                                    print('输入金额不是100的整数倍，请重新输入')
                                    save_money = int(input('请将钞票叠好，并整齐放入存钞口(输入存款金额,最低一百)：'))
                                else:
                                    print('交易正在处理，请稍后。。。')
                                    time.sleep(3)
                                    print('%s 元已成功存入账户 %s\t账户名 %s'%(save_money,user_id,username))
                                    database[username]['balance'] += save_money
                                    with open('log.txt','a') as f:  #写入日志
                                        f.write(str(time.strftime("%Y %b %d %X"))+'\t卡号为 %s 的用户 %s  已存入金额 %d\n'%(user_id,username,save_money))
                                    temp += str(time.strftime("%Y %b %d %X"))+'\t存入金额：%d\n'%save_money

                            elif cont == '3': #转账
                                transfer_id = input('请输入转账帐户卡号：')
                                transfer_user = input('请输入帐户名：')
                                if transfer_id == database[transfer_user]['ID']:
                                    transfer_money = float(input('请输入转账金额：'))

                                    if transfer_money > database[username]['balance']:
                                        print('操作失败，您输入的金额大于您的余额总数')
                                    else:
                                        print('交易正在处理，请稍后。。。')
                                        time.sleep(3)
                                        database[username]['balance'] -= transfer_money
                                        database[transfer_user]['balance'] += transfer_money
                                        with open('log.txt','a') as f:  #写入日志
                                            f.write(str(time.strftime("%Y %b %d %X"))+'\t卡号为 %s 的用户 %s 转出金额为 %d 给卡号为 %s 的用户 %s\n'%(user_id,username,transfer_money,transfer_id,transfer_user))
                                        print('成功转账 %s 给卡号为 %s 的用户 %s'%(transfer_money,transfer_id,transfer_user))
                                        temp += time.strftime("%Y %b %d %X")+'\t向卡号为 %s 的用户 %s 转账 %d \n'%(transfer_id,transfer_user,transfer_money)
                                else:
                                    print('输入的卡号为 %s 的用户名为 %s 账户有误，原因可能账户信息不匹配或被冻结'%(transfer_id,transfer_user))
                            elif cont == '4': #查询
                                print('您的余额为：%.2f'%database[username]['balance'])
                            elif cont == '5': #打印凭条
                                print(temp)

                            elif cont == '6': #退卡
                                print('正在退卡。。')
                                time.sleep(1)
                                print('请取走您的银行卡，感谢使用')
                                ctrl_flag = True
                                break
                            else:
                                print('序号输入有误，可能不存在序号%s 对应的选项'%cont)

                    else:
                        count +=1
                        password = input('输入有误，您还有 %s 次机会\n请重新输入：'%(3-count)).strip()
                else:
                    count +=1
                    password = input('密码仅为6位数字，您还有 %s 次机会\n请重新输入: '%(3-count)).strip()

        with open('log.txt','a') as f1: #写入日志
            f2 = open('database.txt','w')
            f2.write(str(database))
            f1.write(str(time.strftime("%Y %b %d %X"))+'\t修改数据库文件\n')
            f2.close()
