#coding=utf-8

# date      :    2018/12/13 21:12
# Author    :    qimi
# Filename  :    main.py


import os
import re
import json
import pymysql
import time
import sys

attrname = {'devboxinfo': "上线", 'devboxcharge': "上线并充电", 'devcharge': "充电状态", 'devpoweroff': "关机", \
            'devdisconn': "设备异常断开", 'sendmsgwx': "发送微信语音", \
            'sysmsg': "收到系统消息", 'speechplay': "设备唤醒", \
            'class': "课堂", 'music': "儿歌", 'story': "故事", 'classic': "国学", 'wiki': "百科", 'english': "英语", 'yelu': "耶鲁", \
            'music_uyeh class': "天天课堂", 'music_uyeh xxxx': "本地内容", \
            'desktop': "桌面", 'usb udisk': "U盘模式", 'shop_uyeh': "在线内容", 'roobo speech en': "英语对话",
            'roobo translate': "翻译", 'voice_eval': "英语学习", \
            'wechat': "微聊", 'roobo': "对话", 'devroobo': "对话状态", 'setting msg1': "消息", 'setting': "设置",
            'dance_uyeh': "舞蹈", 'dance_uyeh play': "舞蹈演示模式"}

devcharge = ["未充电", "开始充电", "停止充电", "完成充电", "未知状态"]



# 数据连接
def dbOpen(host, dbuser , passwd , dbname):
    # 连接数据库
    db = pymysql.connect(host , dbuser , passwd , dbname)
    # 创建游标
    cursor = db.cursor()
    return db,cursor

# 关闭数据库
def dbClose(db):
    db.close()


# 数据表检测
def dbTableCheck(db , cursor):
    # 日志记录表检测
    sql = "create table if not exists logtable(id int primary key auto_increment , logname varchar(64) NOT NULL , actnum int , lognum int ,logdate varchar(15) , logtime varchar(15), other varchar(128)) charset utf8 collate utf8_general_ci;"
    cursor.execute(sql)

    # 元数据表检测
    # 使用预处理语句创建表
    sql = """CREATE TABLE if not exists useraction (
             id int primary key auto_increment,
             userid  VARCHAR(20) NOT NULL,
             userage  int,
             useract  VARCHAR(32),
             actdescr varchar(64),
             descr1  VARCHAR(200),
             descr2  VARCHAR(200),
             descr3  varchar(200),
             actdate varchar(10),
             acttime varchar(10),
             other CHAR(200)) charset utf8 collate utf8_general_ci;"""
    cursor.execute(sql)


# 获取指定目录下的日志文件
# python 中利用os模块将文件夹中的文件扫描出来
def getLogfile(dirname):

    # for root, dirs, files in os.walk(dirname):
    #     # print("root :", root)
    #     # print("subdir:", dirs)
    #     # print("files:", files)
    # return files

    files = os.listdir(dirname)
    # dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
    # print(files)
    # logfiles.sort(key=lambda x: os.path.gettime(os.path.join("../data", x)))
    # str = logfiles[0].split("_")[1]
    # print(str)
    files = sorted(files, key=lambda x: x.split("_")[1])
    print(files)
    return files
    # logfiles.sort(key=lambda x: x.split("_")[1])
    # print(logfiles)
    # tt = os.path.getmtime(os.path.join("../data" , listdirfiles[0]))
    # print(tt)



# 用户数据行为数据保存
def useractSaveDate(db , cursor , fd , data):
    jsonobj = ""
    datatmp = ""
    try:
        jsonobj = json.loads(data[2])
    except:
        print("json error : ", data)
        datatmp = data[2]
        # data[2] = data[2].replace("\\", " ")
        # 规范格式
        # 主要对转义字符进行处理\\ \/ \b \t \r \n \f \v \' \" \? \0 \ #
        datatmp = datatmp.replace("\\", " ")
        datatmp = datatmp.replace("\/", " ")
        datatmp = datatmp.replace("\b", " ")
        datatmp = datatmp.replace("\t", "    ")
        datatmp = datatmp.replace("\r", " ")
        datatmp = datatmp.replace("\n", " ")
        datatmp = datatmp.replace("\f", "")
        datatmp = datatmp.replace("\v", "")
        # datatmp = datatmp.replace("\'", " ")
        # datatmp = datatmp.replace("\"", " ")
        datatmp = datatmp.replace("\?", "?")
        datatmp = datatmp.replace("\0", " ")
        jsonobj = json.loads(datatmp)
        # jsonobj = json.loads(data[2].replace("\\", ""))
        # print("json error : %s", data)

        # db.rollback()
        # db.close()
        # exit(1)
    # attrname = {'devboxinfo': "上线", 'devboxcharge': "上线并充电", 'devcharge':"充电状态",'devpoweroff': "关机",\
    #              'devdisconn':"设备异常断开" , 'sendmsgwx':"发送微信语音" ,\
    #              'sysmsg':"收到系统消息", 'speechplay':"设备唤醒",\
    #              'class':"课堂", 'music':"儿歌", 'story':"故事",'classic':"国学",'wiki':"百科", 'english':"英语", 'yelu':"耶鲁",\
    #              'music_uyeh class':"天天课堂",'music_uyeh xxxx':"本地内容",\
    #              'desktop':"桌面", 'usb udisk':"U盘模式",'shop_uyeh':"在线内容",'roobo speech en':"英语对话", 'roobo translate':"翻译", 'voice_eval':"英语学习",\
    #              'wechat':"微聊", 'roobo':"对话", 'devroobo':"对话状态", 'setting msg1':"消息", 'setting':"设置", 'dance_uyeh':"舞蹈" , 'dance_uyeh play':"舞蹈演示模式"}
    global attrname
    global devcharge
    cmd = jsonobj['cmd']
    value = jsonobj['value']
    sql = ""
    ret = 1
    # 1.开机消息
    if cmd == 'devboxinfo':
        tmp = 0
        try:
            tmp = value['is_charge']

        except:
            tmp = 0
        if tmp == 0:
            pass
        elif tmp >= 1 and tmp <=3:
            cmd = 'devboxcharge'
        else:
            pass

        sql = "INSERT INTO useraction(userid,\
                                 useract, actdescr, descr1, descr2, descr3, actdate, acttime)\
                                 values (\"%s\" , \"%s\" ,\"%s\" , \"%s\" , \"%s\" , \"%s\" , \"%s\" , \"%s\")" % \
              (jsonobj['id'], cmd , attrname[cmd], value['version'], str(value['status']), value['code'], data[0], data[1])

    # 2.功能使用消息 和4.唤醒播放消息
    elif cmd == 'devusefunc':
        if value['func'] == 'speechplay':
            sql = "INSERT INTO useraction(userid,\
                         useract, actdescr, descr1, descr2, descr3, actdate, acttime)\
                         values (\"%s\" , \"%s\" , \"%s\", \"%s\" , \"%s\" , \"%s\" , \"%s\" , \"%s\")" % \
                  (jsonobj['id'], value['func'], attrname['speechplay'], str(value['type']), value['value'], value['id'], data[0], data[1])

        else:
            actstr = ""
            if "music_uyeh" in value['func']:
                    if value['func'] == 'music_uyeh class':
                        actstr = value['func']
                    else:
                        actstr = "music_uyeh xxxx"
            else:
                actstr = value['func']

            try:
                actstr = attrname[actstr]
            except:
                actstr = "未知功能"


            sql = "INSERT INTO useraction(userid,\
                  useract, actdescr, descr1, actdate, acttime)\
                  values (\"%s\" , \"%s\" ,\"%s\", \"%s\" , \"%s\" , \"%s\")" % \
                      (jsonobj['id'], value['func'], actstr, str(value['onestep']), data[0], data[1])
    # 3.音乐播放消息
    elif cmd == 'devboxmusic':
        sql = "INSERT INTO useraction(userid,\
             useract, actdescr, descr1, descr2, descr3, actdate, acttime)\
             values (\"%s\" , \"%s\" ,\"%s\", \"%s\" , \"%s\" , \"%s\" , \"%s\" , \"%s\")" % \
            (jsonobj['id'], value['appname'], attrname[value['appname']], str(value['type']), value['value'], value['id'],  data[0], data[1])

    # 5.关机消息
    elif cmd == 'devpoweroff':
        sql = "INSERT INTO useraction(userid,\
              useract, actdescr, descr1, actdate, acttime)\
              values (\"%s\" , \"%s\" ,\"%s\", \"%s\" , \"%s\" , \"%s\")" % \
              (jsonobj['id'], cmd , attrname[cmd], value['code'], data[0], data[1])

    # 6.异常断开消息
    elif cmd == 'devdisconn':
        sql = "INSERT INTO useraction(userid,\
              useract, actdescr, descr1, actdate, acttime)\
              values (\"%s\" , \"%s\" ,\"%s\", \"%s\", \"%s\" , \"%s\")" % \
              (jsonobj['id'], cmd, attrname[cmd], value['code'], data[0], data[1])

    # 7.接收到微信消息
    elif cmd == 'sendmsgwx':
        sql = "INSERT INTO useraction(userid,\
              useract, actdescr, actdate, acttime)\
              values (\"%s\" , \"%s\" , \"%s\", \"%s\" , \"%s\")" % \
              (jsonobj['id'], cmd, attrname[cmd], data[0], data[1])
        # 将微信消息写入文本
        fd.write(str(data)+"\n")

    elif cmd == 'sysmsg':
        sql = "INSERT INTO useraction(userid,\
                      useract, actdescr, descr1, actdate, acttime)\
                      values (\"%s\" , \"%s\" , \"%s\", \"%s\", \"%s\" , \"%s\")" % \
              (jsonobj['id'], cmd, attrname[cmd], value['ID'], data[0], data[1])
    elif cmd == 'devroobo':
        sql = "INSERT INTO useraction(userid,\
                              useract, actdescr, descr1, descr2, actdate, acttime)\
                              values (\"%s\" , \"%s\" , \"%s\", \"%s\", \"%d\", \"%s\" , \"%s\")" % \
              (jsonobj['id'], cmd, attrname[cmd], value['content'], value['type'], data[0], data[1])
    elif cmd == 'devcharge':
        tmp1 = value['status']
        if tmp1 >=0 and tmp1 <= 3:
            pass
        else:
            tmp1 = 4
        sql = "INSERT INTO useraction(userid,\
                              useract, actdescr, descr1, descr2, actdate, acttime)\
                              values (\"%s\" , \"%s\" , \"%s\", \"%d\", \"%s\", \"%s\" , \"%s\")" % \
              (jsonobj['id'], cmd, attrname[cmd], value['status'], devcharge[tmp1], data[0], data[1])
    else:
        ret = 0
        print("other msg ", data)

    if ret == 0:
        return ret
    else:
        try:
           # 执行sql语句
           # print(sql)
           cursor.execute(sql)
           # 提交到数据库执行
           # 在这里提交会造成解析需要大量时间
           # db.commit()
           return ret
        except:
           # 如果发生错误则回滚
           print("write db error\n",sql)
           db.rollback()



# 开始解析
def decodeOriginalData(db , cursor ,logfd, filename):
    count = 0
    total = 0
    ret = 0
    pattern = re.compile(r"(\d+-\d+-\d+) (\d+:\d+:\d+)  receive message source:(\{.*\}$)")
    # 打开文件
    with open(filename , "r" , encoding="utf-8") as fd:
        while True:
            strdata = fd.readline()
            if not strdata: #or count > 10:
                break;
            total += 1
            result = re.search(pattern, strdata)
            if result:
                actuser = result.groups()
                # print("data:%s\ndatetime: %s\ndataact:%s" %(actuser[0] , actuser[1] , actuser[2]))
                # 数据保存
                ret = useractSaveDate(db , cursor ,logfd , actuser)
                if ret == 1:
                    count +=1

        # print(strdata)
    db.commit()
    fd.close()
    return count,total

# 查询日志文件是否已经解析过
# 解析过 返回true 否则 false
def isLogfileHadDecode(db , cursor , filename):
    sql = "select count(*) from logtable where logname = \'%s\'" % filename
    print(sql)

    try:
       # 执行sql语句
       cursor.execute(sql)
       results = cursor.fetchall()
       # print(results)
       ret = results[0][0]
       # print(ret)
       # 提交到数据库执行
       # db.commit()
    except:
       # 如果发生错误则回滚
       print("error")
       db.rollback()

    if ret == 0:
        print("the file : %s is not exist " %(filename))
        return False
    else:
        print("the file : %s is exist " % (filename))
        return True


# 将日志文件名保存到数据库中
def recordLogfile(db , cursor , filename , num, total):
    str = filename.split("_")[1]
    sql = "insert into logtable(logname ,actnum ,lognum , logdate , logtime) values(\"%s\" , %d, %d , \"%s\", \"%s\")" %(filename, num, total, str[0:8], str[8:14])

    print(sql)

    try:
        # 执行sql语句
        cursor.execute(sql)

        # # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        print("error")
        db.rollback()




if __name__ == '__main__':
    # print(time.strftime('%Y%m%d',time.localtime(time.time())))
    # str1 = "music_uyeh class"
    # if "hello" in str1:
    #     print("找到了")
    # else:
    #     print("没有找到")

    # dict1 = {'abc':"ABC你好", 'abc d':"hello"}
    # key0 = "abc"
    # key1 = "abc d"
    # print(dict1[key0]+dict1[key1])

    # str = "20181212000020"
    # print(str[0:8])
    # print(str[8:14])
    # print("你好")
    # exit(1)
    # 数据目录
    # datadir = "../data7"

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

    datadir = sys.argv[5]

    # print(str(len(sys.argv)))
    # print(sys.argv)

    daytime = time.strftime('%Y%m%d', time.localtime(time.time()))
    # with open("userlog" + daytime + ".run", "a", encoding="utf-8") as userlogfd:
    userlogfd = open("userlog" + daytime + ".run", "a", encoding="utf-8")
    sys.stdout = userlogfd
    sys.stderr = userlogfd


    # 获取日志文件名
    logfiles = getLogfile(datadir)
    print(logfiles)

    # exit(1)

    # 连接数据库
    # db,cursor = dbOpen("root", "123456", "uyehdb")
    db, cursor = dbOpen(sys.argv[2], sys.argv[3], sys.argv[4], "uyehdb")

    # 数据表检测
    dbTableCheck(db , cursor)



    daytime = time.strftime('%Y%m%d',time.localtime(time.time()))
    # 保存微信消息文件
    with open(datadir+ "/sendwxmsg_"+daytime+".wx", "w", encoding="utf-8") as logfd:
        for logfile in logfiles:
            # print(logfile)
            if(logfile.endswith(".log")):
                # print(logfile)
                ret = isLogfileHadDecode(db, cursor, logfile)
                if not ret:
                    # 开始解析
                    num,total = decodeOriginalData(db, cursor , logfd, datadir+"/"+logfile)
                    # 将日志文件名存到数据库中
                    recordLogfile(db, cursor, logfile , num , total)

    # 关闭文件logfd
    logfd.close()

    db.commit()


    # 关闭数据库
    dbClose(db)

    # 关闭日志输出
    userlogfd.close()
