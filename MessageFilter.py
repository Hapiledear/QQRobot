# -*- coding: utf-8 -*-
# 黑名单机制
import logging

LOGGER = logging.getLogger(__name__)

idList = [1410763408]


def switchToQQ(send_uin):
    # TODO redis缓存对应关系，过期时间为10分钟
    return 0


def filteFromId(send_uin):
    LOGGER.info("send_uin=%d" % send_uin)
    if send_uin == 0:  # 一对一对话，才为0 此时不会出现回文，放行
        return False
    qq = switchToQQ(send_uin)
    if qq in idList:
        LOGGER.info("qq号%d在过滤名单中,此时的u_id=%d" % (qq, send_uin))
        return True
