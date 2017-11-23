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
from db.adStastics import ADStastics

# 加载日志配置
logging.config.fileConfig("conf/log.conf")
logger = logging.getLogger("stastics")

load_dictionary = {}
finish_dictionary = {}
click_dictionary = {}

# 统计开始
def stastics():
    load_dictionary.clear()
    finish_dictionary.clear()
    click_dictionary.clear()
    now = datetime.datetime.now()
    nextStartTime = timeQuarterformat(now)  # 获取当前时间，根据当前时间确定下次开始时间
    starttime = db.getStartTime()  # 本次统计开始的时间
    logger.info('本次开始统计时间:%s', starttime)
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
            stastics()# 读取下一天的日志
        else:
            nexttime = timeQuarterformat(nextStartTime)
            db.updateLastTime(str(nexttime))


endQuarter = None

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
    #2017-11-22 11:19:25,874#INFO#http-8019-exec-5#load#129#143#201#jrtt##101.231.117.234#
    collect_time = timeQuarterformat(time)
    key = param[4] + param[5] + param[6] + collect_time.strftime('%Y-%m-%d %H:%M:%S') # key格式：gameid + id + type +统计时间段的开始时间
    ads = None
    if load_dictionary.has_key(key):
        ads = load_dictionary.get(key)
    else:
        ads = ADStastics()
        ads.id = param[5]
        ads.gameId = param[4]
        ads.type = param[6]
        ads.collect_datetime = collect_time
        ads.source = param[7]
        ads.subsource = param[8]
    ads.load += 1
    if ads.ipLoad.count(param[9]) == 0:
        ads.ipLoad.append(param[9])
    load_dictionary[key] = ads # 新增或更新dict


# 统计加载完成
def stasticsFinish(param, time):
    #2017-11-22 11:19:25,874#INFO#http-8019-exec-5#load#129#143#201#jrtt##101.231.117.234#
    collect_time = timeQuarterformat(time)
    key = param[4] + param[5] + param[6] + collect_time.strftime('%Y-%m-%d %H:%M:%S') # key格式：gameid + id + type +统计时间段的开始时间
    ads = None
    if finish_dictionary.has_key(key):
        ads = finish_dictionary.get(key)
    else:
        ads = ADStastics()
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
    finish_dictionary[key] = ads # 新增或更新dict


# 统计点击
def stasticsClick(param, time):
    #2017-11-22 11:19:25,874#INFO#http-8019-exec-5#load#129#143#201#jrtt##101.231.117.234#
    collect_time = timeQuarterformat(time)
    key = param[4] + param[5] + param[6] + collect_time.strftime('%Y-%m-%d %H:%M:%S') # key格式：gameid + id + type +统计时间段的开始时间
    ads = None
    if click_dictionary.has_key(key):
        ads = click_dictionary.get(key)
    else:
        ads = ADStastics()
        ads.id = param[5]
        ads.gameId = param[4]
        ads.type = param[6]
        ads.collect_datetime = collect_time
        ads.source = param[7]
        ads.subsource = param[8]
    ads.click += 1
    if ads.ipclick.count(param[9]) == 0:
        ads.ipclick.append(param[9])
    click_dictionary[key] = ads # 新增或更新dict

# 保存统计结果
def savedicts():
    global endQuarter
    logger.info("当前统计时间段为：%s" % endQuarter)
    for key in load_dictionary:
        db.saveStastics(load_dictionary[key])
    for key in finish_dictionary:
        db.saveStastics(finish_dictionary[key])
    for key in click_dictionary:
        db.saveStastics(click_dictionary[key])
    load_dictionary.clear()
    finish_dictionary.clear()
    click_dictionary.clear()


# 获取所给时间前一刻钟的时间点
def timeQuarterformat(time):
    minu = 0
    minute = time.minute
    if minute < 15:
        minu = 0
    elif minute < 30:
        minu = 15
    elif minute < 45:
        minu = 30
    else:
        minu = 45
    date = time.strftime('%Y-%m-%d %H:')
    return datetime.datetime.strptime(date + str(minu) + ":00", '%Y-%m-%d %H:%M:%S')
