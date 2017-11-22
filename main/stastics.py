# -*- coding:UTF-8 -*-
'''
Created on 2017年11月21日

@author: zhaiyl
'''

import logging.config
import db.MysqlDB as db
from file.getFile import getFilename
from datetime import datetime

#加载日志配置
logging.config.fileConfig("conf/log.conf")
logger = logging.getLogger("stastics")

#统计开始
def stastics():
    now = datetime.now()
    maxTime = timeformat(now)
    lasttime = db.getLastTime();
    logger.info(lasttime)
    filename = getFilename(lasttime)
    logger.info(filename)
    try:
        fo = open(filename)
        #逐行读取日志,判断时间是否满足
        for line in fo.readlines():
            param = line.split("#")
            time = datetime.strptime(param[0],'%Y-%m-%d %H:%M:%S,%f');
            if cmp(time, maxTime) <= 0:
                handleLine(param)
    except IOError :
        logger.info('file not found:%s', filename)

#解析每一行日志
def handleLine(param):
    if param == None:
        return
    if param[3] == 'load':
        stasticsLoad(param)
    elif param[3] == 'finish':
        stasticsFinish(param)
    elif param[3] == 'click':
        stasticsClick(param)
    else:
        return

#统计加载
def stasticsLoad(param):
    return

#统计加载完成
def stasticsFinish(param):
    return

#统计点击
def stasticsClick(param):
    return

#获取所给时间前一刻钟的时间点
def timeformat(time):
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
    return datetime.strptime(date + str(minu) + ":00",'%Y-%m-%d %H:%M:%S')