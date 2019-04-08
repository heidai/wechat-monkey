# -*- coding: utf-8 -*-
# filename: cron.py

from tools import AccessToken

class RefreshAccessToken(object):
    def GET(self):
        try:
            accessToken = AccessToken()
            accessToken.Refresh()
            return "success"
        except Exception, ex:
            print "RefreshAccessToken.Get error: %s" % (ex)
            return 'fail'