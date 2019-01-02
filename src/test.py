#coding=utf-8

# date      :    2018/12/11 23:18
# Author    :    qimi
# Filename  :    test.py

import os
import re
import json
import sys
import time
import pymysql
# import demjson








# python 中利用os模块将文件夹中的文件扫描出来
def getlogfile(dirname):

    for root, dirs, files in os.walk(dirname):
        # print("root :", root)
        # print("subdir:", dirs)
        # print("files:", files)
        return files


if __name__ == '__main__':
    # files = getlogfile("../data")
    # print(files)




    # 参数判断
    argvlen = len(sys.argv)
    if argvlen != 6:
        if argvlen == 0:
            pass
        else:
            print("请运行主程序...")
            os.system('pause')
            sys.exit(-1)
    else:
        if sys.argv[1] != 'uyehuser':
            print("sb")
            sys.exit(-1)

    # print(str(len(sys.argv)))
    # print(sys.argv)

    daytime = time.strftime('%Y%m%d', time.localtime(time.time()))
    # with open("userlog" + daytime + ".run", "a", encoding="utf-8") as userlogfd:
    userlogfd = open("userlog" + daytime + ".run", "a", encoding="utf-8")
    sys.stdout = userlogfd
    sys.stderr = userlogfd

    # 打开文件
    count = 0
    # pattern = re.compile(r"\d-\d-\d \d:\d:\d.*receive message source:")
    pattern = re.compile(r"(\d+-\d+-\d+) (\d+:\d+:\d+)  receive message source:(\{.*\}$)")
    # pattern = re.compile("(^\d.*b\}$)", flags=0)
    str1 = r'2018-11-30 10:14:35  receive message source:{"cmd":"devusefunc" , "value":{"func":"desktop" , "onestep":0} , "type":1 , "id":"3060100000000048" ,"flag":0 ,"src":1}'
    # str1 = '2018-11-30 10:14:35 {cmd:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab}'
    print(str1)
    # print(len(str1))

    result = re.search(pattern , str1 , 0)
    # result = pattern.match(str1)
    print(result)
    print(result.groups())
    actdate1, acttime1, action1 = result.groups()
    # data = data[2]
    # print(data)

    jsonobj = json.loads(action1)

    print(jsonobj['cmd'])



    # value = jsonobj['value']['func']
    value = jsonobj['value']['func']
    print(value)
    try:
        print(jsonobj['value']['id'])
    except:
        jsonobj['value']['func'] = "hello"
        print(jsonobj['value'])

    print("hello ",jsonobj['value'])

    testdata = ('2018-12-27', '18:51:17', '{"cmd":"devroobo" , "value":{"content":"我大家来Nini\\Aro路我来了" , "type":1} , "type":1 , "id":"3060100000004601" ,"flag":0 ,"src":1}')

    jsonobj = json.loads(testdata[2].replace("\\", " "))
    # jsonobj = demjson.encode(testdata[2])

    # print(jsonobj)
    print("jsonobj:",jsonobj['value'])

    # 关闭日志输出
    userlogfd.close()

    # os.system('pause')



# print(type(jsonobj))

# # 连接数据库
# db = pymysql.connect("localhost" , "root" , "123456" , "uyehdb")
# # 创建游标
# cursor = db.cursor()
#
# # 使用 execute()  方法执行 SQL 查询
# cursor.execute("SELECT VERSION()")
#
# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
#
# print("Database version : %s " % data)


# 创建数据库表
# # 使用 execute() 方法执行 SQL，如果表存在则删除
# cursor.execute("DROP TABLE IF EXISTS  useraction")
#
# # 使用预处理语句创建表
# sql = """CREATE TABLE useraction (
#          userid  VARCHAR(20) NOT NULL,
#          action  VARCHAR(32),
#          descr1  VARCHAR(200),
#          descr2  VARCHAR(200),
#          descr3  varchar(200),
#          actdate varchar(10),
#          acttime varchar(10),
#          other CHAR(200))"""
#
# cursor.execute(sql)
# values('1010', 'desktop', '0', '', '', '2018-12-12', '10:14:35', '')"
# 数据库插入
# SQL 插入语句
# print(jsonobj['id'])
# a = "12345"
# sql = "INSERT INTO useraction(userid,\
#          action, descr1, descr2, descr3, actdate, acttime, other)\
#          values (\"%s\" , \"%s\" , \"%s\" , \"%s\" , \"%s\" , \"%s\" , \"%s\" , \"%s\")" % \
#          (jsonobj['id'], 'desktop', '0', a, '0',  actdate1, acttime1, '0')

# print(sql)
#
# try:
#    # 执行sql语句
#    cursor.execute(sql)
#    # 提交到数据库执行
#    db.commit()
# except:
#    # 如果发生错误则回滚
#    print("error")
#    db.rollback()
#
#
# # 关闭数据库连接
# db.close()



# with open("../data/"+files[0] , "r" , encoding="utf-8") as fd:
#     while True:
#         count += 1
#         str = fd.readline()
#         if not str or count > 10:
#             break;
#         print(str)









