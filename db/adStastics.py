# -*- coding:UTF-8 -*-
'''
Created on 2017年11月23日

@author: zhaiyl
'''

class ADStastics(object):
    '''
    广告统计数据
    '''
    id = 0
    gameId = 0
    type = 0
    source = '' # 渠道
    subsource = '' # 子渠道
    load = 0 # 展示数
    finish = 0 # 展示完成数
    click = 0 # 点击数
    ipLoad = [] # 独立展示ip
    ipfinish = [] #独立完成ip
    ipclick = [] # 独立点击ip
    collect_datetime = None # 统计时间段的开始时间
    load_time = 0 #总加载时间
    

    def __init__(self):
        '''
        Constructor
        '''
        