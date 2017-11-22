# -*- coding:UTF-8 -*-
'''
Created on 2017年11月21日

@author: zhaiyl
'''
import MySQLdb
import conf.conf as conf

#获取最后统计的时间
def getLastTime():
    conn = MySQLdb.connect(host = conf.host,
                           port = conf.port,
                           user = conf.user,
                           passwd = conf.passwd,
                           db = conf.db)
    cur = conn.cursor();
    cur.execute('select * from time_control where server = ' + str(conf.server))
    data = cur.fetchone()
    cur.close()
    conn.commit()
    conn.close()
    return data[2]

#修改最后统计时间
def updateLastTime(lasttime):
    conn = MySQLdb.connect(host = conf.host,
                           port = conf.port,
                           user = conf.user,
                           passwd = conf.passwd,
                           db = conf.db)
    cur = conn.cursor();
    cur.execute('update time_control set time=' + lasttime
                 + ' where server=' + str(conf.server))
    cur.close()
    conn.commit()
    conn.close()
    