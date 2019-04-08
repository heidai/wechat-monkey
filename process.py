# -*- coding: utf-8 -*-
# filename: process.py


import xml.etree.ElementTree as ET

from chatrobot import ChatRobot
from event import Event


class Process(object): # 处理模块，根据MsgType调用相应处理模块
    def __init__(self, webData):
        self.__xmlData = ET.fromstring(webData)

    def Do(self): #启动事件处理
        try:
            msgType = self.__xmlData.find('MsgType').text # 消息类型
            if msgType == 'event': # 事件处理
                event = Event(self.__xmlData)
                return event.Do()
            else: # 消息处理
                robot = ChatRobot(self.__xmlData)
                return robot.Do()
        except Exception, ex:
            print "Process.Do error: %s" % (ex)
            return ''
