# coding:utf-8
import json
import logging

import requests

T_Api_key = "5bf9369732de46ea9526afd405c2fd64"
T_Api_url = "http://www.tuling123.com/openapi/api"

LOGGER = logging.getLogger(__name__)


def getMsgFromTuring(msg, usrId='00001'):
    LOGGER.info("请求图灵机器人,msg=%s" % msg)
    jsonData = {"key": T_Api_key, "info": msg, "userid": usrId}
    response = requests.post(T_Api_url, json=jsonData)
    LOGGER.info("返回结果=%s" % response.text)
    resJson = response.json()
    resCode = resJson["code"]
    resMsg = resJson["text"]
    if resCode == 100000:  # 文本类
        pass
    elif resCode == 200000:  # 链接类
        resMsg = resMsg + "链接=" + resJson["url"]
        pass
    elif resCode == 302000:  # 新闻类
        newsList = resJson["list"]
        resMsg += "\r\n"
        for news in newsList:
            resMsg += "标题：" + news["article"] + "\n链接" + news["detailurl"]
        pass
    elif resCode == 308000:  # 菜谱类
        newsList = resJson["list"]
        resMsg += "\r\n"
        for news in newsList:
            resMsg += "做法" + news["info"] + "\n链接" + news["detailurl"]
        pass
    return resMsg
