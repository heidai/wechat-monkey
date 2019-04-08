# -*- coding: utf-8 -*-
# filename: chatrobot.py

import threading

from baiduimageclassify import BaiduImageClassify
from baidustt import BaiduSTT
from msgreceive import MsgReceive
from msgreply import MsgReply
from tools import MediaIdAndMediaURL, switch
from tuling import TulingRobot


class ChatRobot(object):
    def __init__(self, xmlData):
        self.__msgReceive = MsgReceive() # 处理接收数据
        self.__msgReceive.ParseMsg(xmlData) # 解析收到的消息
        self.__msgReply = MsgReply(self.__msgReceive.fromUserName, self.__msgReceive.toUserName) # 处理发送数据
        self.__tulingRobot = TulingRobot(self.__msgReceive.fromUserName) # 图灵机器人

    def Do(self):
        def ImageClassify(mediaId): # 图像识别
            mediaIdAndURL = MediaIdAndMediaURL() # 资源文件上传下载
            filePath, picUrl = mediaIdAndURL.GetMediaURL('image', mediaId) # 通过微信mediaId下载文件，生成新浪云url
            classify = BaiduImageClassify()
            classify.ImageClassify(filePath)
        try:
            for case in switch(self.__msgReceive.msgType):
                if case('text'): # 文本消息
                    msg = self.__msgReceive.content
                    response = self.__tulingRobot.ChatText(msg)
                    break
                if case('image'): # 图片消息，暂不支持
                    # 启动异步线程分析图片
                    new_thread = threading.Thread(target=ImageClassify,args=(self.__msgReceive.mediaId,))
                    new_thread.start()
                    #filePath, picUrl = mediaIdAndURL.GetMediaURL('image', self.__msgReceive.mediaId)
                    #response = self.__tulingRobot.ChatImage(picUrl) #tuling暂不支持
                    response = [{'MsgType': 'text', 'Values': u'我看破，我不说。'}]
                    break
                if case('voice'): # 语音消息，免费版图灵不支持语音，此处调用百度语音进行转换
                    if len(self.__msgReceive.recognition) > 0 : # 使用微信语音识别结果
                        msg = self.__msgReceive.recognition
                        print "wechatSTT: %s" % (msg)
                    else: # 使用百度语音识别
                        if self.__msgReceive.format != 'amr':
                            raise Exception('Not support voice format "%s"' % (self.__msgReceive.format))
                        self.__mediaIdAndURL = MediaIdAndMediaURL() # 资源文件上传下载
                        filePath, voiceUrl = self.__mediaIdAndURL.GetMediaURL('voice', self.__msgReceive.mediaId) # 通过微信mediaId下载文件，生成新浪云url
                        self.__baiduSTT = BaiduSTT(self.__msgReceive.fromUserName) # 百度语音识别
                        msg = self.__baiduSTT.STT(filePath)
                        print "baiduSTT: %s" % (msg)
                    response = self.__tulingRobot.ChatText(msg)
                    break
                if case('location'): # 地理位置消息，图灵暂不支持，此处当成文本方式，只传地理位置信息
                    msg = u'地址：' + self.__msgReceive.label
                    response = self.__tulingRobot.ChatText(msg)
                    break
                if case('link'): # 链接消息，图灵暂不支持，此处当成文本方式，只传标题+描述信息
                    msg = self.__msgReceive.title + self.__msgReceive.description
                    response = self.__tulingRobot.ChatText(msg)
                    break
                if case('video'): # 视频消息
                    pass
                if case('shortvideo'): # 小视频消息
                    pass
                if case():
                    response = self.__tulingRobot.ChatAll(self.__msgReceive.msgType, '')
                    break
            
            for item in response:
                if item['MsgType'] in ['image', 'voice', 'video']:
                    filePath, item['MediaId'] = self.__mediaIdAndURL.GetMediaID(item['MsgType'], item['Values'])
            
            return self.__msgReply.PackMsg(response)
        except Exception, ex:
            print 'ChatRobot.Chat error: %s' % (ex)
            return self.__msgReply.PackMsg([{'MsgType':'text', 'Values': u'抱歉, 小猴子还没学会该项技能,请稍后再试试...'}])
