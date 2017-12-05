# -*- coding:UTF-8 -*-
'''
Created on 2017年11月21日

@author: zhaiyl
'''
import logging.config
from main.stastics import stastics
import time
import threading

# 加载日志配置
logging.config.fileConfig("conf/log.conf")
logger = logging.getLogger("stastics")

'''
统计启动入口
15分钟统计一次
'''
if __name__ == '__main__':
    try:
        while True:
            _thread = threading.Thread(target=stastics(),args=())
            _thread.setDaemon(True)
            _thread.start()
            time.sleep(15 * 60);
    except:
        logger.exception("Exception Logged")
