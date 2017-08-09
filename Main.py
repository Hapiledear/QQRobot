# -*- coding: utf-8 -*-
import logging
import threading
from Login import Login, loopPool
from logConfig import setup_logging

logger = logging.getLogger(__name__)
setup_logging()
login = Login()
if login.login():
    getMessageThread = threading.Thread(target=loopPool())
    getMessageThread.start()



