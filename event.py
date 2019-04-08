# -*- coding: utf-8 -*-
# filename: event.py

import time

from tools import switch

class Event(object): # wechat event处理
    def __init__(self, xmlData):
        self.__xmlData = xmlData
        self.__event = self.__xmlData.find('Event').text # event类型
        self.__dict = dict()
        self.__dict['ToUserName'] = self.__xmlData.find('FromUserName').text
        self.__dict['FromUserName'] = self.__xmlData.find('ToUserName').text
        self.__dict['CreateTime'] = int(time.time())

    def Do(self):
        try:
            for case in switch(self.__event):
                if case('subscribe'): # 关注
                    print u"粉丝[%s]关注公众账号" % (self.__dict['ToUserName'])
                    self.__dict['Content'] = u'欢迎关注，小猴子已掌握生活百科知识，学会了很多技能，能帮您查天气、菜谱、列车、油价、股票，还会算数、中英互译。能陪您聊天逗乐，简直是居家旅行必备[Smirk]...'.encode("utf-8")
                    return self.__FormatXmlText()
                    break
                if case('unsubscribe'): # 取消关注
                    print u"粉丝[%s]取消关注公众账号" % (self.__dict['ToUserName'])
                    return 'success'
                    break
                if case('MASSSENDJOBFINISH'): # 群发消息结果
                    status = self.__xmlData.find('Status').text # 群发的结果
                    totalCount = self.__xmlData.find('TotalCount').text # group_id下粉丝数；或者openid_list中的粉丝数
                    filterCount = self.__xmlData.find('FilterCount').text # 过滤（过滤是指，有些用户在微信设置不接收该公众号的消息）后，准备发送的粉丝数，原则上，FilterCount = SentCount + ErrorCount
                    sentCount = self.__xmlData.find('SentCount').text # 发送成功的粉丝数
                    errorCount = self.__xmlData.find('ErrorCount').text # 发送失败的粉丝数
                    print u"群发消息[%s]，粉丝总数%s，群发送粉丝%s，成功%s，失败%s" % (status, totalCount, filterCount, sentCount, errorCount)
                if case():
                    return 'success'
                    break
        except Exception, ex:
            print "Event.Do error: %s" % (ex)
            return ''

    def __FormatXmlText(self):
        XmlForm = """
        <xml>
            <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
            <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
            <CreateTime>{CreateTime}</CreateTime>
            <MsgType><![CDATA[text]]></MsgType>
            <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)