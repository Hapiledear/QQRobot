# -*- coding: utf-8 -*-
import json
import logging
import re

import datetime

import requests

from GlobalParam import chunks, BackMsg

regex = r"(?<=知乎日报)[\s]?\d*"
nowDate = datetime.datetime.now().strftime("%Y%m%d")
NOW_NEWS = "https://news-at.zhihu.com/api/4/news/{0}"
LATIEST_NEWS = "https://news-at.zhihu.com/api/4/news/before/{0}"
SHARE_NEWS = "https://daily.zhihu.com/story/{0}"

header_info = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}

LOGGER = logging.getLogger(__name__)


def getUrl(msg):
    LOGGER.debug("接收到到消息%s" % msg)
    matches = re.findall(regex, msg)
    if len(matches) == 0 or len(matches[0]) == 0 or nowDate in matches[0]:
        return NOW_NEWS.format("latest")
    else:
        return LATIEST_NEWS.format(matches[0].strip())


def getResMsg(response):
    if response.status_code == 404:
        return "请输入正确的日期"
    elif response.status_code == 200:
        resMSg = ["内容如下:\n"]
        for stories in chunks(response.json()["stories"],6):
            msg = ""
            for story in stories:
                msg += "标题：" + story["title"]
                msg += "\n链接：" + SHARE_NEWS.format(story["id"])
                msg += "\r\n"
            resMSg.append(msg)
        return resMSg
    else:
        print "错误代码 %d" % response.status_code
        return "未知错误，请稍后再试"


def getMsgFromZhihuDaly(msg, id):
    url = getUrl(msg.encode("utf-8"))
    LOGGER.info("知乎日报req url=%s" % url)
    response = requests.get(url, headers=header_info)
    resMsg = getResMsg(response)
    # LOGGER.info("返回消息 = %s" % resMsg)
    resMsgObj = BackMsg(resMsg, id)
    return resMsgObj

