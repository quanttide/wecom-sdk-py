# -*- coding: utf-8 -*-

import datetime
import time

class WeChatWorkSDKException(Exception):
    def __init__(self, errcode, errmsg):
        self.errcode = errcode
        self.errmsg = errmsg

    def __str__(self):
        return "WeChatWorkSDK Error {errcode}: {errmsg}".format(errcode=self.errcode, errmsg=self.errmsg)

class WeChatWorkError(Exception):
    def __init__(self,variable,length):
        self.variable = variable
        self.length = length
    #检查是否超出规定长度
    def overlength(variable,length):
        variable = str(variable)
        # length = int(length)
        if variable is not None:
            assert len(variable) < length
    # 检查是否短于规定长度
    def lesslength(variable,length):
        variable = str(variable)
        if variable is not None:
            assert len(variable) > length
    # 用于处理get_active_stat函数，因为仅可以处理三十天内的数据
    def dateRange():
        beginDate = (datetime.datetime.now() - datetime.timedelta(days = 30))
        otherStyleTime = beginDate.strftime("%Y-%m-%d")
        dates = []
        endDate = time.strftime("%Y-%m-%d", time.localtime())
        dt = datetime.datetime.strptime(otherStyleTime, "%Y-%m-%d")
        date = otherStyleTime[:]
        while date <= endDate:
            dates.append(date)
            dt = dt + datetime.timedelta(1)
            date = dt.strftime("%Y-%m-%d")
        return dates
    def write_config(data):
        f = open('_config.py','a+')
        f.write(data)
        f.close()