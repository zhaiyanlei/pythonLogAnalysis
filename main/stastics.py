# -*- coding:UTF-8 -*-
'''
Created on 2017年11月21日

@author: zhaiyl
'''

import logging.config
import db.MysqlDB as db
from file.getFile import getFilename
import datetime
import os
from db.adStatistic import ADStatistics

# 加载日志配置
logging.config.fileConfig("conf/log.conf")
logger = logging.getLogger("stastics")

statistic_dictionary = {}
endQuarter = None


# 统计开始
def stastics():
    global endQuarter
    statistic_dictionary.clear()
    now = datetime.datetime.now()
    nextStartTime = timeQuarterformat(now)  # 获取当前时间，根据当前时间确定下次开始时间
    starttime = db.getStartTime()  # 本次统计开始的时间
    logger.info('本次开始统计时间:%s', starttime)
    startQuarter = timeQuarterformat(starttime)
    endQuarter = startQuarter + datetime.timedelta(minutes=15)
    filename = getFilename(starttime)  # 获取当前需要统计的日志文件
    if not os.path.exists(filename):  # 文件不存在
        logger.info('文件不存在:%s,统计的开始时间为%s', filename, starttime)
        if cmp(starttime.strftime('%Y-%m-%d'), nextStartTime.strftime('%Y-%m-%d')) >= 0:
            # 本次开始时间与下次开始时间相同，认为是当天文件不存在，返回
            return
        else:
            # 本次开始统计时间不是当天，文件不存在即跳过该天的日志，开始日期+1的日志
            starttime = starttime + datetime.timedelta(days=1)
            db.updateLastTime(starttime.strftime('%Y-%m-%d'))
            stastics()
            return;
    endtime = timeQuarterformat(nextStartTime)  # 本次统计结束的时间
    logger.info("开始解析配置文件：%s,统计的开始时间为%s", filename, starttime)
    try:
        fo = open(filename)
        # 逐行读取日志,判断时间是否满足
        for line in fo.readlines():
            param = line.split("#")
            time = datetime.datetime.strptime(param[0], '%Y-%m-%d %H:%M:%S,%f')  # 解析日志中的时间
            if time < starttime:
                continue
            if time < nextStartTime:
                handleLine(param, time)
                endtime = timeQuarterformat(time)
    except IOError :
        logger.info('file not found:%s', filename)
        db.updateLastTime(str(endtime))
    finally:
        savedicts()
        # 保存最后统计时间，
        if cmp(starttime.strftime('%Y-%m-%d'), nextStartTime.strftime('%Y-%m-%d')) < 0:
            nexttime = endtime + datetime.timedelta(days=1)
            nexttime = datetime.datetime(nexttime.year, nexttime.month, nexttime.day, 0, 0, 0)
            db.updateLastTime(str(nexttime))
            stastics()  # 读取下一天的日志
        else:
            nexttime = timeQuarterformat(nextStartTime)
            db.updateLastTime(str(nexttime))


# 解析每一行日志
def handleLine(param, time):
    if param == None:
        return
    global endQuarter
    if endQuarter == None:
        startQuarter = timeQuarterformat(time)
        endQuarter = startQuarter + datetime.timedelta(minutes=15)
    if time >= endQuarter:
        savedicts()
        db.updateLastTime(str(endQuarter))
        startQuarter = timeQuarterformat(time)
        endQuarter = startQuarter + datetime.timedelta(minutes=15)
    
    if param[3] == 'load':
        stasticsLoad(param, time)
    elif param[3] == 'finish':
        stasticsFinish(param, time)
    elif param[3] == 'click':
        stasticsClick(param, time)
    else:
        return


# 统计加载
def stasticsLoad(param, time):
    # 2017-11-22 11:19:25,874#INFO#http-8019-exec-5#load#129#143#201#jrtt##101.231.117.234#
    collect_time = timeQuarterformat(time)
    key = param[4] + param[5] + param[6] + collect_time.strftime('%Y-%m-%d %H:%M:%S')  # key格式：gameid + id + type +统计时间段的开始时间
    if statistic_dictionary.has_key(key):
        ads = statistic_dictionary.get(key)
    else:
        ads = ADStatistics()
        ads.id = param[5]
        ads.gameId = param[4]
        ads.type = param[6]
        ads.collect_datetime = collect_time
        ads.source = param[7]
        ads.subsource = param[8]
    ads.load += 1
    if ads.ipLoad.count(param[9]) == 0:
        ads.ipLoad.append(param[9])
    statistic_dictionary[key] = ads  # 新增或更新dict


# 统计加载完成
def stasticsFinish(param, time):
    # 2017-11-22 11:19:25,874#INFO#http-8019-exec-5#load#129#143#201#jrtt##101.231.117.234#
    collect_time = timeQuarterformat(time)
    key = param[4] + param[5] + param[6] + collect_time.strftime('%Y-%m-%d %H:%M:%S')  # key格式：gameid + id + type +统计时间段的开始时间
    if statistic_dictionary.has_key(key):
        ads = statistic_dictionary.get(key)
    else:
        ads = ADStatistics()
        ads.id = param[5]
        ads.gameId = param[4]
        ads.type = param[6]
        ads.collect_datetime = collect_time
        ads.source = param[7]
        ads.subsource = param[8]
    ads.finish += 1
    ads.load_time += int(param[10])
    if ads.ipfinish.count(param[9]) == 0:
        ads.ipfinish.append(param[9])
    statistic_dictionary[key] = ads  # 新增或更新dict


# 统计点击
def stasticsClick(param, time):
    # 2017-11-22 11:19:25,874#INFO#http-8019-exec-5#load#129#143#201#jrtt##101.231.117.234#
    collect_time = timeQuarterformat(time)
    key = param[4] + param[5] + param[6] + collect_time.strftime('%Y-%m-%d %H:%M:%S')  # key格式：gameid + id + type +统计时间段的开始时间
    if statistic_dictionary.has_key(key):
        ads = statistic_dictionary.get(key)
    else:
        ads = ADStatistics()
        ads.id = param[5]
        ads.gameId = param[4]
        ads.type = param[6]
        ads.collect_datetime = collect_time
        ads.source = param[7]
        ads.subsource = param[8]
    ads.click += 1
    if ads.ipclick.count(param[9]) == 0:
        ads.ipclick.append(param[9])
    statistic_dictionary[key] = ads  # 新增或更新dict


# 保存统计结果
def savedicts():
    global endQuarter
    logger.info("当前统计时间段为：%s,统计结果数量为：%s" % (endQuarter, len(statistic_dictionary)))
    for key in statistic_dictionary:
        db.saveStastics(statistic_dictionary[key])
    statistic_dictionary.clear()


# 获取所给时间前一刻钟的时间点
def timeQuarterformat(time):
    minute = time.minute
    minu = minute / 15 * 15
    date = time.strftime('%Y-%m-%d %H:')
    return datetime.datetime.strptime(date + str(minu) + ":00", '%Y-%m-%d %H:%M:%S')


if __name__ == '__main__':
    print "请从start.py开始执行"
