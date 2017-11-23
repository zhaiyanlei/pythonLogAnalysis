# -*- coding:UTF-8 -*-
'''
Created on 2017年11月21日

@author: zhaiyl
'''
import MySQLdb
import conf.conf as conf
import ConfigParser


# 获取最后统计的时间
def getStartTime():
    cf = get_cf()
    conn = getConn(cf)
    cur = conn.cursor();
    cur.execute('select * from time_control where server = ' + str(conf.server))
    data = cur.fetchone()
    cur.close()
    conn.commit()
    conn.close()
    return data[2]


# 修改最后统计时间
def updateLastTime(lasttime):
    cf = get_cf()
    conn = getConn(cf)
    cur = conn.cursor();
    cur.execute("update time_control set time='" + lasttime
                 + "' where server=" + str(conf.server))
    cur.close()
    conn.commit()
    conn.close()


def saveStastics(ads):
    sql = "insert into ad_stastics(apk_channel_id, game_id, type, source, subsource,\
     visit, finish, click, ipload, ipfinish, ipclick, collect_datetime, load_time) \
     values('%s','%s','%s', '%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
    cf = get_cf()
    conn = getConn(cf)
    cur = conn.cursor();
    cur.execute(sql % (ads.id, ads.gameId, ads.type, ads.source, ads.subsource, ads.load, \
                ads.finish, ads.click, len(ads.ipLoad), len(ads.ipfinish), len(ads.ipclick), ads.collect_datetime, ads.load_time))
    cur.close()
    conn.commit()
    conn.close()


#######数据库配置#######
def get_cf():
        cf = ConfigParser.ConfigParser()
        cf.read(conf.db_conf_path)
        return cf


# 获取数据库主机名
def getHost(cf):
    return cf.get('db', 'host')


# 获取数据库端口号
def getPort(cf):
    return cf.get('db', 'port')


# 获取数据库用户名
def getUser(cf):
    return cf.get('db', 'user')


# 获取数据库密码
def getPasswd(cf):
    return cf.get('db', 'passwd')


# 获取数据库名称
def getDbName(cf):
    return cf.get('db', 'dbName')


# 获取数据库连接
def getConn(cf):
    conn = MySQLdb.connect(host=getHost(cf),
                           port=int(getPort(cf)),
                           user=getUser(cf),
                           passwd=getPasswd(cf),
                           db=getDbName(cf));
    return conn
