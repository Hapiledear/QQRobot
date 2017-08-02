# coding:utf-8

GET_QR_CODE_URL = r"https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=0&l=M&s=5&d=72&v=4&t=0.1"
VERIFY_QR_CODE = ("https://ssl.ptlogin2.qq.com/ptqrlogin?"
                  "ptqrtoken={0}&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106&"
                  "u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&"
                  "ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&dumy=&fp=loginerroralert&0-0-157510&"
                  "mibao_css=m_webqq&t=undefined&g=1&js_type=0&js_ver=10184&login_sig=&pt_randsalt=3")
VERIFY_QR_CODE_REF = ("https://ui.ptlogin2.qq.com/cgi-bin/login?"
                      "daid=164&target=self&style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&"
                      "s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001")

GET_VFWEBQQ = "http://s.web2.qq.com/api/getvfwebqq?ptwebqq={0}&clientid=53999199&psessionid=&t=0.1"
GET_VFWEBQQ_REF = "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"

GET_UIN_AND_PSESSIONID = "http://d1.web2.qq.com/channel/login2"
GET_UIN_AND_PSESSIONID_REF = "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"

POLL_MESSAGE = "http://d1.web2.qq.com/channel/poll2"
POLL_MESSAGE_REF = "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"

SEND_MESSAGE_TO_FRIEND = "http://d1.web2.qq.com/channel/send_buddy_msg2"
SEND_MESSAGE_TO_FRIEND_REF = "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"

SEND_MESSAGE_TO_DISCUSS = "http://d1.web2.qq.com/channel/send_discu_msg2"
SEND_MESSAGE_TO_DISCUSS_REF = "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"

SEND_MESSAGE_TO_GROUP = "http://d1.web2.qq.com/channel/send_qun_msg2"
SEND_MESSAGE_TO_GROUP_REF = "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2"


def build_url(url, params):
    return url.format(params)
