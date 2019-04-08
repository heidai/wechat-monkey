# -*- coding: utf-8 -*-
# filename: msgreply.py

import time

from tools import switch

class MsgReply(object): # 处理发送给用户的消息
    def __init__(self, toUserName, fromUserName):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
  
    def PackMsg(self, L):
        MsgType = {'text':False, 'url':False, 'image':False, 'voice':False, 'video':False, 'news':False}
        try:
            for item in L:
                for case in switch(item['MsgType']):
                    if case('text'):
                        MsgType['text'] = True
                        self.__dict['MsgType'] = 'text'
                        self.__dict['Text'] = item['Values'].encode("utf-8")
                        break
                    if case('url'):
                        MsgType['url'] = True
                        self.__dict['MsgType'] = 'text'
                        self.__dict['Url'] = item['Values'].encode("utf-8")
                        break
                    if case('image'):
                        MsgType['image'] = True
                        self.__dict['MsgType'] = 'image'
                        self.__dict['MediaId'] = item['MediaId']
                        break
                    if case('voice'):
                        MsgType['voice'] = True
                        self.__dict['MsgType'] = 'voice'
                        self.__dict['MediaId'] = item['MediaId']
                        break
                    if case('video'):
                        MsgType['video'] = True
                        self.__dict['MsgType'] = 'video'
                        self.__dict['MediaId'] = item['MediaId']
                        break
                    if case('news'):
                        MsgType['news'] = True
                        self.__dict['news'] = item['Values']
                        break
                    if case():
                        raise Exception('ERROR')
            if MsgType['news']:
                return self.__FormatXmlNews()
            elif MsgType['image'] or MsgType['voice'] or MsgType['video']:
                return self.__FormatXmlMedia()
            elif MsgType['url'] and MsgType['text']:
                self.__dict['ArticleCount'] = 1
                self.__dict['Title'] = self.__dict['Text']
                return self.__FormatXmlLink()
            elif MsgType['url']:
                self.__dict['Content'] = self.__dict['Url']
                return self.__FormatXmlText()
            elif MsgType['text']:
                self.__dict['Content'] = self.__dict['Text']
                return self.__FormatXmlText()
            else:
                raise Exception('ERROR')
        except Exception, ex:
            print "MsgReply.PackMsg error: %s" % (ex)
            self.__dict['MsgType'] = 'text'
            self.__dict['Content'] = u'抱歉, 小猴子还没学会该项技能,请稍后再试试...'.encode("utf-8")
            return self.__FormatXmlText()
    
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
	
    def __FormatXmlLink(self):
        XmlForm = """
        <xml>
            <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
            <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
            <CreateTime>{CreateTime}</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>{ArticleCount}</ArticleCount>
            <Articles>
                <item>
                    <Title><![CDATA[{Title}]]></Title>
                    <Description><![CDATA[{Url}]]></Description>
                    <PicUrl></PicUrl>
                    <Url><![CDATA[{Url}]]></Url>
                </item>
            </Articles>
        </xml>
        """
        return XmlForm.format(**self.__dict)
    
    def __FormatXmlMedia(self):
        XmlForm = """
        <xml>
            <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
            <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
            <CreateTime>{CreateTime}</CreateTime>
            <MsgType><![CDATA[{MsgType}]]></MsgType>
            <MediaId><![CDATA[{MediaId}]]></MediaId>
        </xml>
        """
        return XmlForm.format(**self.__dict)

    def __FormatXmlNews(self): # 目前wechat限制只能发送1条图文消息
        def XmlNews(L):
            articles = ''
            i = 1
            for item in L:
                articles += "%d.%s%s\n" % (i, item['Title'].encode("utf-8"), item['Url'].encode("utf-8"))
                i += 1
                if i >= 8: # 最大8条消息
                    break
            return articles, L[0]['Url']
        self.__dict['Articles'], self.__dict['Url']= XmlNews(self.__dict['news'])
        XmlForm = """
        <xml>
            <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
            <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
            <CreateTime>{CreateTime}</CreateTime>
            <MsgType><![CDATA[news]]></MsgType>
            <ArticleCount>1</ArticleCount>
            <Articles>
                <item>
                <Title><![CDATA[{Text}]]></Title>
                <Description><![CDATA[{Articles}]]></Description>
                <PicUrl></PicUrl>
                <Url><![CDATA[{Url}]]></Url>
                </item>
            </Articles>
        </xml>
        """
        return XmlForm.format(**self.__dict)