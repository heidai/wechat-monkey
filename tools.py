# -*- encoding=utf-8 -*- s
# filename: tools.py

import datetime
import json
import os
import urllib

import pylibmc
import requests

from sae.storage import Bucket


"""
class AccessToken(object): # 获取wechat access token
    def __init__(self):
        self.__url = 'https://api.weixin.qq.com/cgi-bin/token'
        self.__appid = '' # 开发者ID(AppID)
        self.__secret = '' # 开发者密码(AppSecret)
        self.__memcached = pylibmc.Client()
        self.__accessToken = ''
        
    def Refresh(self):
        try:
            payload_access_token = {
                'grant_type': 'client_credential', 
                'appid': self.__appid, 
                'secret': self.__secret
            }
            r = requests.get(self.__url, params = payload_access_token)
            dict_result= (r.json())
            if 'errcode' in dict_result: # 获取失败
                print "Get access token from wechat failed[errcode: %s, errmsg: %s]" % (dict_result['errcode'], dict_result['errmsg'])
            else: # 获取成功
                self.__accessToken = dict_result['access_token']
        except Exception, ex:
            print "AccessToken.Refresh error: %s" % (ex)
        finally:
            self.__memcached.set('AccessToken', self.__accessToken) # 将access token存入Memcached
            print "AccessToken.Refresh access token: %s" % (self.__accessToken)
    
    def Get(self):
        self.__accessToken = self.__memcached.get('AccessToken')
        if self.__accessToken == None:
            self.Refresh()
        print "AccessToken.Get access token: %s" % (self.__accessToken)
        return self.__accessToken
"""


class AccessToken(object): # 获取wechat access token
    def __init__(self):
        self.__url = 'https://api.weixin.qq.com/cgi-bin/token'
        self.__appid = '' # 开发者ID(AppID)
        self.__secret = '' # 开发者密码(AppSecret)
        self.__memcached = pylibmc.Client()
        self.__now = datetime.datetime.now()
        
    def Refresh(self):
        try:
            payload_access_token = {
                'grant_type': 'client_credential', 
                'appid': self.__appid, 
                'secret': self.__secret
            }
            r = requests.get(self.__url, params = payload_access_token)
            dict_result= (r.json())
            if 'errcode' in dict_result: # 获取失败
                print "Get access token from wechat failed[errcode: %s, errmsg: %s]" % (dict_result['errcode'], dict_result['errmsg'])
                self.__accessToken = ''
                self.__memcached.delete('AccessToken')
                self.__memcached.delete('Expires')
                self.__memcached.delete('LastTime')
            else: # 获取成功
                self.__accessToken = dict_result['access_token']
                self.__expires = dict_result['expires_in']
                self.__memcached.set('AccessToken', self.__accessToken)
                self.__memcached.set('Expires', self.__expires)
                self.__memcached.set('LastTime', self.__now)
        except Exception, ex:
            print "AccessToken.Refresh error: %s" % (ex)
    
    def Get(self):
        def IsOutofDate(old, now, expires): # 过期返回True
            if (now - old).seconds > (expires - 300): # 提前300s刷新
                return True
            else:
                return False
        self.__accessToken = self.__memcached.get('AccessToken')
        self.__expires = self.__memcached.get('Expires')
        self.__lastTime = self.__memcached.get('LastTime')
        if (self.__accessToken == None) or (self.__expires == None) or IsOutofDate(self.__lastTime, self.__now, int(self.__expires)):
            self.Refresh()
        print "AccessToken.Get access token: %s" % (self.__accessToken)
        return self.__accessToken


class MediaIdAndMediaURL(object): # MediaId及MediaURL获取转换
    def __init__(self):
        self.__accessToken = self.__GetAccessToken() # 获取微信access token

    def __GetAccessToken(self):
        accessToken = AccessToken()
        return accessToken.Get()

    def __WechatUpload(self, fileType, filePath):
        try:
            urlUpload = 'http://file.api.weixin.qq.com/cgi-bin/media/upload'
            upload = {
                'access_token': self.__accessToken,
                'type': fileType
            }
            bucket = Bucket('wechat')
            fileName = os.path.basename(filePath)
            data = {'media':(fileName, bucket.get_object_contents(filePath))}
            r = requests.post(url = urlUpload, params = upload, files = data)
            dictResult = r.json()
            #print dictResult
            mediaId = dictResult['media_id']
            #print mediaId
            return mediaId
        except Exception, ex:
            print 'MediaIdAndMediaURL.__WechatUpload error:%s' % (ex)
            return ''
    
    def __WechatDownload(self, fileType, mediaID): # 下载微信资源，并返回新浪云url
        try:
            urlDownload = 'http://file.api.weixin.qq.com/cgi-bin/media/get'
            download = {
                'access_token': self.__accessToken,
                'media_id': mediaID
            }
            r = requests.get(url = urlDownload, params = download)
            #print "status_code: %s" % (r.status_code)
            #print "headers:"
            #print r.headers
            if 'Content-disposition' in r.headers:
                disposition = r.headers['Content-disposition']
                print "disposition:%s" % (disposition)
                fileName = disposition[disposition.find('filename="') + 10:-1]
            else:
                if fileType == 'image':
                    fileName = mediaID + '.jpg'
                else:
                    fileName = mediaID + '.amr'
            #print "fileName:%s" % (fileName)
            bucket = Bucket('wechat')
            filePath = 'filecache/' + fileType + '/' + fileName
            bucket.delete_object(filePath)
            bucket.put_object(filePath, r.content)
            #print "filePath:%s" % (filePath)
            return filePath
        except Exception, ex:
            print 'MediaIdAndMediaURL.__WechatDownload error:%s' % (ex)
            return ''
    
    def __TulingDownload(self, fileType, urlDownload): # 下载tuling资源，并返回新浪云路径
        try:
            fileName = os.path.basename(urlDownload)
            r = requests.get(url = urlDownload)
            #print fileName
            bucket = Bucket('wechat')
            filePath = 'filecache/' + fileType + '/' + fileName
            bucket.delete_object(filePath)
            bucket.put_object(filePath, r.content)
            return filePath
        except Exception, ex:
            print 'MediaIdAndMediaURL.__TulingDownload error:%s' % (ex)
            return ''

    def GetMediaURL(self, fileType, mediaID): # 通过MediaID下载微信资源，并生成新浪云URL
        try:
            print 'GetMediaURL[fileType: %s, mediaID: %s]' % (fileType, mediaID)
            filePath = self.__WechatDownload(fileType, mediaID)
            bucket = Bucket('wechat')
            fileURL = bucket.generate_url(filePath)
            #print fileURL
            return filePath, fileURL
        except Exception, ex:
            print 'MediaIdAndMediaURL.GetMediaURL error:%s' % (ex)
            return ''
    
    def GetMediaID(self, fileType, MediaURL): # 通过URL下载图灵资源，并上传微信获取MediaID
        try:
            print 'GetMediaID[fileType: %s, MediaURL: %s]' % (fileType, MediaURL)
            filePath = self.__TulingDownload(fileType, MediaURL)
            mediaID = self.__WechatUpload(fileType, filePath)
            #print mediaID
            return filePath, mediaID
        except Exception, ex:
            print 'MediaIdAndMediaURL.GetMediaID error:%s' % (ex)
            return ''


# This class provides the functionality we want. You only need to look at
# this if you want to know how this works. It only needs to be defined
# once, no need to muck around with its internals.
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

if __name__ == '__main__':
    accessToken = AccessToken()
    print accessToken.Get()
