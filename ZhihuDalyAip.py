# -*- coding: utf-8 -*-
import json
import logging
import re

import datetime

import requests


regex = r"(?<=知乎日报)\S*"
nowDate = datetime.datetime.now().strftime("%Y%m%d")
NOW_NEWS = "https://news-at.zhihu.com/api/4/news/{0}"
LATIEST_NEWS = "https://news-at.zhihu.com/api/4/news/before/{0}"
SHARE_NEWS = "https://daily.zhihu.com/story/{0}"


header_info = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}

LOGGER = logging.getLogger(__name__)



def getUrl(msg):
    matches = re.findall(regex, msg)
    if len(matches) == 0:
        return NOW_NEWS.format("latest")
    elif nowDate in matches[0] or '' in matches[0]:
        return NOW_NEWS.format("latest")
    else:
        return LATIEST_NEWS.format(matches[0].strip())


def getResMsg(response):
    if response.status_code == 404:
        return "请输入正确的日期"
    elif response.status_code == 200:
        resMSg = "内容如下:\r\n"
        for story in response.json()["stories"]:
            resMSg += "标题：" + story["title"]
            resMSg += "\n链接：" + SHARE_NEWS.format(story["id"])
            resMSg += "\r\n"
        return resMSg
    else:
        print "错误代码 %d" % response.status_code
        return "未知错误，请稍后再试"


def getMsgFromZhihuDaly(msg):
    url = getUrl(msg)
    LOGGER.info("req url=%s" % url)
    response = requests.get(url,headers=header_info)
    resMsg = getResMsg(response)
    LOGGER.info("返回消息 = %s" % resMsg)
    return resMsg
