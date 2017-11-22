# -*- coding:UTF-8 -*-
'''
Created on 2017年11月21日

@author: zhaiyl
'''
from main.stastics import stastics
import time


'''
统计启动入口
15分钟统计一次
'''
if __name__ == '__main__':
    while True:
        stastics()
        time.sleep(1 * 60);
