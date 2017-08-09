# -*- coding: utf-8 -*-

import json
import logging
import webbrowser

import os
import requests
import time

import ApiUrl
import GlobalParam
from GlobalParam import session
from MessageObjects import MsgResponse, msgCallBack

import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
LOGGER = logging.getLogger(__name__)

header_info = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
session.headers.update(header_info)


class Login(object):
    def login(self):
        self.getQrCode()
        url = self.verifyQRCode()
        self.getPtwebqq(url)
        self.getVfwebqq()
        self.getUinAndPsessionid()
        LOGGER.info("-----------登陆成功!%s----------" % GlobalParam.uin)
        return True

    def getQrCode(self):
        LOGGER.info("获取二维码图片")
        with open("qrcode.png", "wb") as qrCodeImg:
            response = session.get(ApiUrl.GET_QR_CODE_URL)  # get请求方式，并设置请求头
            qrCodeImg.write(response.content)  # 获得二进制得请求体，并写入png文件
            GlobalParam.qrsig = response.cookies['qrsig']  # 获取cookies
            path = os.getcwd() + "/qrcode.png"
        LOGGER.info("二维码已保存,请打开手机QQ并扫描二维码,%s" % path)
        LOGGER.debug("res cookies=%r" % response.cookies)
        # webbrowser.open_new_tab("file://" + path)  # 使用浏览器打开二维码图片

    def verifyQRCode(self):
        LOGGER.info("等待扫描二维码")
        while True:
            time.sleep(1)
            LOGGER.info("qrsig=%s hash=%s" % (GlobalParam.qrsig, hash33(GlobalParam.qrsig)))
            reqUrl = ApiUrl.build_url(ApiUrl.VERIFY_QR_CODE, hash33(GlobalParam.qrsig))
            LOGGER.info("url=%s" % reqUrl)
            response = session.post(reqUrl, headers={"Referer": ApiUrl.VERIFY_QR_CODE_REF})
            res = response.text
            LOGGER.info("response=%s" % res)
            LOGGER.debug("res cookies=%r" % response.cookies)
            if "成功" in res:
                for content in res.split("','"):
                    if content.startswith("http"):
                        LOGGER.info("正在登录，请稍后")
                        return content
            elif r"已失效" in res:
                LOGGER.info("二维码已失效，尝试重新获取二维码")
                self.getQrCode()
            elif "403 Forbidden" in res:
                LOGGER.info("请求失败，请检查请求参数")
                raise Exception("403 Forbidden")

    def getPtwebqq(self, url):
        LOGGER.info("开始获取ptwebqq")
        GlobalParam.ptwebqq = session.cookies["ptwebqq"]
        LOGGER.debug("开始check_sig? cookies=%r" % session.cookies)
        LOGGER.info("url=%s" % url)
        response = session.get(url)
        LOGGER.info("status=%s" % response.status_code)
        LOGGER.debug("res cookies=%r" % response.cookies)

    def getVfwebqq(self):
        LOGGER.info("开始获取vfwebqq")
        LOGGER.debug("开始获取vfwebqq cookies=%r" % session.cookies)

        reqUrl = ApiUrl.build_url(ApiUrl.GET_VFWEBQQ, GlobalParam.ptwebqq)
        LOGGER.info("url=%s" % reqUrl)
        session.headers.update({"Referer": ApiUrl.GET_VFWEBQQ_REF})
        response = session.get(reqUrl)

        retryTimes4Vfwebqq = 3
        LOGGER.info("status=%s" % response.status_code)
        while response.status_code == 404 and retryTimes4Vfwebqq > 0:
            response = ApiUrl.build_url(ApiUrl.GET_VFWEBQQ, GlobalParam.ptwebqq)
            retryTimes4Vfwebqq = retryTimes4Vfwebqq - 1
        LOGGER.info("resJson = %s " % response.json())
        vfwebqq = response.json()["result"]["vfwebqq"]
        LOGGER.debug("res cookies=%r" % response.cookies)

    def getUinAndPsessionid(self):
        LOGGER.info("开始获取uin和psessionid")
        reqData = {"ptwebqq": GlobalParam.ptwebqq, "clientid": 53999199, "psessionid": "", "status": "online"}
        reqParams = {"r": json.dumps(reqData)}
        session.headers.update({"Referer": ApiUrl.GET_UIN_AND_PSESSIONID_REF, "Origin": "http://d1.web2.qq.com"})

        LOGGER.debug("cookies=%r" % session.cookies)
        LOGGER.info("url=%s" % ApiUrl.GET_UIN_AND_PSESSIONID)
        LOGGER.info("formData=%r" % reqParams)
        # LOGGER.info("formData=%s" % json.dumps(reqParams, indent=4, sort_keys=True))
        # cookie中的关键参数 p_skey=c9mecHyxJQpWASH41ChFe5ZSVF0T9fGtn1S*uYr0xws_;
        # 需要前几个步骤中的cookie
        response = session.post(ApiUrl.GET_UIN_AND_PSESSIONID, data=reqParams)

        LOGGER.debug("res cookies=%r" % response.cookies)
        LOGGER.info("resJson = %s " % response.text)
        GlobalParam.psessionid = response.json()["result"]["psessionid"]
        GlobalParam.uin = response.json()["result"]["uin"]
        LOGGER.info("获取到到psessionId=%s,uin=%s" % (GlobalParam.psessionid, GlobalParam.uin))


def loopPool():
    while True:
        LOGGER.info("开始接收消息")
        reqData = {"ptwebqq": GlobalParam.ptwebqq, "clientid": 53999199, "psessionid": GlobalParam.psessionid,
                   "key": ""}
        reqParams = {"r": json.dumps(reqData)}
        session.headers.update({"Referer": ApiUrl.POLL_MESSAGE_REF, "Origin": "http://d1.web2.qq.com"})
        response = session.post(ApiUrl.POLL_MESSAGE, data=reqParams)
        resJson = json.loads(response.text, object_hook=MsgResponse)
        LOGGER.info("res = %s " % response.text)
        if "errmsg" in response.text:
            # 执行退出操作，重新登陆一遍
            LOGGER.info("轮训超时 sts=%d" % response.status_code)
            pass
        else:
            msgCallBack(resJson)


def hash33(s):
    e = 0
    n = len(s)
    for i in range(n):
        if i == 0:
            a = e
        a += (a << 5) + ord(s[i])
    res = 2147483647 & a
    # LOGGER.info("resHash=%s" % res)
    return res
