# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web

from process import Process


class Handle(object):        
    def POST(self):
        try:
            webData = web.data()
            print "Receive from user: %s" % (webData)
            process = Process(webData)
            msg = process.Do()
            print "Reply to user: %s" % (msg)
            return msg
        except Exception, Argment:
            return Argment
    
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, world"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "monkey2019" #请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument