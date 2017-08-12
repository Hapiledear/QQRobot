# -*- coding: utf-8 -*-
import logging
import threading
from Login import Login, loopPool
from logConfig import setup_logging



import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
logger = logging.getLogger(__name__)
setup_logging()
login = Login()
if login.login():
    getMessageThread = threading.Thread(target=loopPool())
    getMessageThread.start()



