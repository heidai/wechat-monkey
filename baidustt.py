# -*- encoding=utf-8 -*- s
# filename: baidustt.py

import os

from aip import AipSpeech

from sae.storage import Bucket


"""
语音转文字
"""
class BaiduSTT(object):
    def __init__(self, OpenID):
        self.__AppID = self.__get_AppID() # 百度AppID
        self.__APIKey = self.__get_APIKey() # 百度APIKey
        self.__SecretKey = self.__get_SecretKey() # 百度SecretKey
        self.__format = 'amr' # 语音文件的格式
        self.__rate = '8000' # 采样率，微信采样率8000
        self.__cuid = OpenID # 用户唯一标识，用来区分用户，填写微信OpenID，长度为60以内
        self.__dev_pid = '1537' # 不填写lan参数生效，都不填写，默认1537（普通话 输入法模型）
        self.__client = AipSpeech(self.__AppID, self.__APIKey, self.__SecretKey)

    def __get_AppID(self): # 百度AppID
        return '14998128'
    
    def __get_APIKey(self): # 百度APIKey
        return 'maUfjhtuP3LBrfXmBsfyhtIF'
    
    def __get_SecretKey(self): # 百度SecretKey
        return '6xhMVKhpI7rSzHu7koO8H6GVr0y17wK5'

    def STT(self, filePath): # 输入语音文件（amr格式），输出文字
        try:
            bucket = Bucket('wechat')
            result = self.__client.asr(bucket.get_object_contents(filePath), self.__format, self.__rate, {'cuid': self.__cuid,
                                                                                                  'dev_pid': self.__dev_pid})
            if 'error_code' in result: # 识别失败
                raise Exception("error_code: %s, error_msg: %s" % (result['error_code'], result['error_msg']))
            return result['result'][0] # 提供1-5个候选结果，utf-8 编码
        except Exception, ex:
            print 'BaiduSTT.STT error:%s' % (ex)
            return ''