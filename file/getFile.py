# -*- coding:UTF-8 -*-
'''
Created on 2017年11月21日

@author: zhaiyl
'''
import datetime
from conf import conf

# 获取当前需要统计的文件
def getFilename(lasttime):
    now = datetime.datetime.now()
    nowStr = now.strftime('%Y-%m-%d');
    start = lasttime
    startStr = start.strftime('%Y-%m-%d');
    if (nowStr != startStr):
        filename = conf.filepath + conf.filename + "." + startStr
    else:
        filename = conf.filepath + conf.filename
    return filename

#获取早先文件
def getPreviousFile(time):
    filename = conf.filepath + "." + time;
    return filename
    