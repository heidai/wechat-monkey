# -*- coding: utf-8 -*-
# filename: msgreceive.py

from tools import switch


class MsgReceive(object): # 处理接收到的用户消息
    def __init__(self):
        pass

    def ParseMsg(self, xmlData): # 解析xml
        try:
            self.__xmlData = xmlData
            self.toUserName = self.__xmlData.find('ToUserName').text # 开发者微信号
            self.fromUserName = self.__xmlData.find('FromUserName').text # 发送方帐号（一个OpenID）
            self.createTime = self.__xmlData.find('CreateTime').text # 消息创建时间 （整型）
            self.msgType = self.__xmlData.find('MsgType').text # 消息类型
            self.MsgId = self.__xmlData.find('MsgId').text # 消息id，64位整型

            for case in switch(self.msgType):
                if case('text'): # 文本消息
                    self.content = self.__xmlData.find('Content').text.encode("utf-8") # 文本消息内容
                    break
                if case('image'): # 图片消息
                    self.mediaId = self.__xmlData.find('MediaId').text # 消息媒体id，可以调用多媒体文件下载接口拉取数据
                    break
                if case('voice'): # 语音消息
                    self.mediaId = self.__xmlData.find('MediaId').text # 消息媒体id，可以调用多媒体文件下载接口拉取数据
                    self.format = self.__xmlData.find('Format').text # 语音格式，如amr，speex等
                    self.recognition = self.__xmlData.find('Recognition').text
                    if self.recognition != None:
                        self.recognition = self.recognition.encode("utf-8") # 语音识别结果，UTF8编码，如开启语音识别则存在
                    else:
                        self.recognition = ''
                    break
                if case('video'): # 视频消息
                    self.mediaId = self.__xmlData.find('MediaId').text # 消息媒体id，可以调用多媒体文件下载接口拉取数据
                    self.thumbMediaId = self.__xmlData.find('ThumbMediaId').text # 视频消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据
                    break
                if case('shortvideo'): # 小视频消息
                    self.mediaId = self.__xmlData.find('MediaId').text # 消息媒体id，可以调用多媒体文件下载接口拉取数据
                    self.thumbMediaId = self.__xmlData.find('ThumbMediaId').text # 视频消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据
                    break
                if case('location'): # 地理位置消息
                    self.location_X = self.__xmlData.find('Location_X').text # 地理位置维度
                    self.location_Y = self.__xmlData.find('Location_Y').text # 地理位置经度
                    self.scale = self.__xmlData.find('Scale').text # 地图缩放大小
                    self.label = self.__xmlData.find('Label').text # 地理位置信息
                    break
                if case('link'): # 链接消息
                    self.title = self.__xmlData.find('Title').text # 消息标题
                    self.description = self.__xmlData.find('Description').text # 消息描述
                    self.url = self.__xmlData.find('Url').text # 消息链接
                    break
                if case():
                    pass
                    break
        except Exception, ex:
            print "MsgReceive.ParseMsg error: %s" % (ex)
            return ''
