# -*- encoding=utf-8 -*- s
# filename: tuling.py

import json
import requests

from tools import switch


"""
图灵机器人
"""
class TulingRobot(object):
    def __init__(self, OpenID):
        self.__url = 'http://openapi.tuling123.com/openapi/api/v2' # 图灵API url
        self.__apiKey = 'a323758630ff4d6dacf72d90b316fc3c' # apiKey,机器人标识
        self.__userId = self.__GetUserId(OpenID) # userId,用户唯一标识
        #self.__province, self.__city = self.__GetLocation() # 获取地理位置

    def __GetUserId(self, OpenID):  # userId,用户唯一标识不超过32位长度，目前微信OpenID长度为28
        tmp = ''
        for char in OpenID:
            if (char >= '0' and char <= '9') or (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
                tmp += char
        return tmp

    def __GetLocation(self):  # 获取地理位置，待获取用户地理位置
        return u'上海', u'上海'

    def __FormatRequestText(self, text): # 文本
        body = {
            "reqType": 0,
            "perception": {
                "inputText": {
                    "text": text
                }
            },
            "userInfo": {
                "apiKey": self.__apiKey,
                "userId": self.__userId
            }
        }
        return json.dumps(body)
    
    def __FormatRequestImage(self, url): # 图片
        body = {
            "reqType": 1,
            "perception": {
                "inputImage": {
                    "url": url
                }
            },
            "userInfo": {
                "apiKey": self.__apiKey,
                "userId": self.__userId
            }
        }
        return json.dumps(body)

    def __FormatRequestVoice(self, url): # 音频
        body = {
            "reqType": 2,
            "perception": {
                "inputMedia": {
                    "url": url
                }
            },
            "userInfo": {
                "apiKey": self.__apiKey,
                "userId": self.__userId
            }
        }
        return json.dumps(body)

    def __FormatRespond(self, respond):
        def FormatMsg(msgType, values):
            return {'MsgType':msgType, 'Values':values[msgType]}
        def FormatNews(values):
            L = []
            for news in values['news']:
                if len(news['name']) > 0:
                    L.append({'MsgType':'news', 'Title':news['name'], 'PicUrl':news['icon'], 'Url':news['detailurl']})
            return {'MsgType':'news', 'Values':L}
        
        L = []
        for results in respond:
            resultType = results['resultType']
            values = results['values']
            for case in switch(resultType):
                if case('text'):
                    L.append(FormatMsg('text', values))
                    break
                if case('url'):
                    L.append(FormatMsg('url', values))
                    break
                if case('voice'):
                    L.append(FormatMsg('voice', values))
                    break
                if case('video'):
                    L.append(FormatMsg('video', values))
                    break                 
                if case('image'):
                    L.append(FormatMsg('image', values))
                    break  
                if case('news'):
                    L.append(FormatNews(values))
                    break
                if case():
                    L.append({'MsgType':'text', 'Values':u'抱歉, 小猴子还没学会该项技能,请稍后再试试...'})
                    break
        return L
    
    def __chat(self, msgType, msg):
        try:
            body = ''
            for case in switch(msgType):
                if case('text'): # 文本消息
                    body = self.__FormatRequestText(msg)
                    break
                if case('image'): # 图片消息
                    body = self.__FormatRequestImage(msg)
                    break
                if case('voice'): # 语音消息
                    body = self.__FormatRequestVoice(msg)
                    break
                if case():
                    raise Exception('ERROR')
                    break

            if len(body) > 0:
                print "Send to Tuling: %s" % (body)
                r = requests.post(self.__url, data = body)
                respond = json.loads(r.text)
                print "Recvice from Tuling: %s" % (respond)
                respond = self.__FormatRespond(respond['results'])
                """
                for item in respond:
                    if item['MsgType'] == 'news':
                        for news in item['Values']:
                            print "MsgType:%s, Title:%s, PicUrl:%s, Url:%s" % (news['MsgType'], news['Title'], news['PicUrl'], news['Url'])
                    else:
                        print "MsgType:%s, Values:%s" % (item['MsgType'], item['Values'])
                """
                return respond
            else:
                raise Exception('ERROR') 
        except Exception:
            return [{'MsgType':'text', 'Values': u'抱歉, 小猴子还没学会该项技能,请稍后再试试...'}]
    
    def ChatText(self, msg): # 文本聊天
        return self.__chat('text', msg)

    def ChatImage(self, url): # 图片聊天
        return self.__chat('image', url)
    
    def ChatVoice(self, url): # 语音聊天
        return self.__chat('voice', url)

    def ChatAll(self, msgType, msg): # 其他方式聊天
        return self.__chat(msgType, msg)