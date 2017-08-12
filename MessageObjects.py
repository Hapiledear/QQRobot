# -*- coding: utf-8 -*-
import json
import logging
import re
import types

import ApiUrl
import GlobalParam
from GlobalParam import session
from MessageRouter import getReturnMessage

LOGGER = logging.getLogger(__name__)


class MsgResponse(object):
    def __init__(self, d):
        self.__dict__ = d

    # 消息来源 message 好友消息 group_message 群消息  discu_message 讨论组消息
    def get_poll_type(self):
        return self.result[0].poll_type

    # 发送者ID 用于回复消息
    def get_from_uin(self):
        return self.result[0].value.from_uin

    # 消息内容
    def get_content(self):
        resStr = ""
        for str in self.result[0].value.content[1:]:
            if isinstance(str, list):
                pass
            else:
                resStr = resStr + str
        return resStr


def msgCallBack(msgResponse):
    LOGGER.info("回复消息")
    type = msgResponse.get_poll_type()
    id = msgResponse.get_from_uin()
    msg = msgResponse.get_content()

    if type == "message":  # 策略:有求必回
        callBack_message(id, msg)
    elif type == "group_message" and msg.startswith(r"@玄姬"):  # @自己才回
        callBack_group_message(id, msg)
    elif type == "discu_message" and msg.startswith(r"@玄姬"):
        callBack_discu_message(id, msg)
        pass


def callBack_message(id, msg):
    msgObj = getReturnMessage(msg, id)
    if msgObj.onlyOneMsg():
        sendPsnMsg(id, msgObj.msgs)
    else:
        for sendMsg in msgObj.msgs:
            sendPsnMsg(id, sendMsg)


def sendPsnMsg(id, msg):
    LOGGER.info("发送消息【%s】给好友[%s]" % (msg, id))
    reqContent = [msg, ["font", {"color": "000000", "name": "微软雅黑", "size": 10, "style": [0, 0, 0]}]]
    reqParam = {"to": id, "content": json.dumps(reqContent), "face": 573, "clientid": 53999199, "msg_id": 65890001,
                "psessionid": GlobalParam.psessionid}
    reqData = {"r": json.dumps(reqParam)}
    response = postWithRetry(ApiUrl.SEND_MESSAGE_TO_FRIEND, reqData, refUrl=ApiUrl.SEND_MESSAGE_TO_FRIEND_REF,
                             origin="http://d1.web2.qq.com")
    checkSendMsgResult(response)


def callBack_group_message(id, msg):
    msgObj = getReturnMessage(msg, id)
    if msgObj.onlyOneMsg():
        sendGroupMsg(id, msgObj.msgs)
    else:
        for sendMsg in msgObj.msgs:
            sendGroupMsg(id, sendMsg)


def sendGroupMsg(id, msg):
    LOGGER.info("发送消息【%s】给群[%s]" % (msg, id))
    reqContent = [msg, ["font", {"color": "000000", "name": "微软雅黑", "size": 10, "style": [0, 0, 0]}]]
    reqParam = {"group_uin": id, "content": json.dumps(reqContent), "face": 573, "clientid": 53999199,
                "msg_id": 65890001,
                "psessionid": GlobalParam.psessionid}
    reqData = {"r": json.dumps(reqParam)}
    response = postWithRetry(ApiUrl.SEND_MESSAGE_TO_GROUP, reqData, refUrl=ApiUrl.SEND_MESSAGE_TO_GROUP_REF,
                             origin="http://d1.web2.qq.com")
    checkSendMsgResult(response)


def callBack_discu_message(id, msg):
    msgObj = getReturnMessage(msg, id)
    if msgObj.onlyOneMsg():
        sendDiscuMsg(id, msgObj.msgs)
    else:
        for sendMsg in msgObj.msgs:
            sendDiscuMsg(id, sendMsg)


def sendDiscuMsg(id, msg):
    LOGGER.info("发送消息【%s】给讨论组[%s]" % (msg, id))
    reqContent = [msg, ["font", {"color": "000000", "name": "微软雅黑", "size": 10, "style": [0, 0, 0]}]]
    reqParam = {"did": id, "content": json.dumps(reqContent), "face": 573, "clientid": 53999199, "msg_id": 65890001,
                "psessionid": GlobalParam.psessionid}
    reqData = {"r": json.dumps(reqParam)}
    response = postWithRetry(ApiUrl.SEND_MESSAGE_TO_DISCUSS, reqData, refUrl=ApiUrl.SEND_MESSAGE_TO_DISCUSS_REF,
                             origin="http://d1.web2.qq.com")
    checkSendMsgResult(response)


def postWithRetry(url, data, refUrl=None, origin=None):
    updateHeaders(refUrl=refUrl, origin=origin)
    LOGGER.info("post url=%s" % url)
    LOGGER.info("data=%r" % data)
    response = session.post(url, data=data)
    times = 1
    while times < 5 and response.status_code != 200:
        LOGGER.info("发送失败，重试次数%d" % times)
        response = session.post(url, data=data)
        times = times + 1
    LOGGER.info("发送消息res sts=%d content=%s" % (response.status_code, response.text))
    return response


def updateHeaders(refUrl=None, origin=None):
    header_info = {"Referer": refUrl, "Origin": origin}
    session.headers.update(header_info)


def checkSendMsgResult(response):
    if response.status_code != 200:
        LOGGER.info("发送失败，Http返回码[%d]" % response.status_code)
        errCode = response.json("errCode")
        if errCode is not None and errCode == 0:
            LOGGER.info("发送成功")
        else:
            LOGGER.info("发送失败，Api返回码[%d]" % response.json["retcode"])
