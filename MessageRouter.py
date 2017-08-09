# -*- coding: utf-8 -*-

# 回复消息的选择器
from TuringRobotApi import getMsgFromTuring
from ZhihuDalyAip import getMsgFromZhihuDaly


def getReturnMessage(msg, id):
    if "知乎日报" in msg:
        return getMsgFromZhihuDaly(msg)
    else:
        return getMsgFromTuring(msg, id)
