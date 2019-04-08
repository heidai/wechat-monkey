# -*- encoding=utf-8 -*- s
# filename: baiduimageclassify.py

from aip import AipImageClassify

from sae.storage import Bucket


"""
语音图像识别
"""
class BaiduImageClassify(object):
    def __init__(self):
        self.__AppID = self.__get_AppID() # 百度AppID
        self.__APIKey = self.__get_APIKey() # 百度APIKey
        self.__SecretKey = self.__get_SecretKey() # 百度SecretKey
        self.__client = AipImageClassify(self.__AppID, self.__APIKey, self.__SecretKey)
    
    def __get_AppID(self): # 百度AppID
        return '15564545'
    
    def __get_APIKey(self): # 百度APIKey
        return 'eTQu0rFLAo18fQC6WN1kgNaG'
    
    def __get_SecretKey(self): # 百度SecretKey
        return 'fjtIgD7auNmWwEOqmOL9grdHCQSZmb7m'

    def ImageClassify(self, filePath):
        try:
            """ 读取图片 """
            bucket = Bucket('wechat')
            image = bucket.get_object_contents(filePath)

            """ 调用通用物体识别 """
            self.__client.advancedGeneral(image)

            """ 如果有可选参数 """
            options = {}
            options["baike_num"] = 0

            """ 带参数调用通用物体识别 """
            info = self.__client.advancedGeneral(image, options)
            #print info
            if 'error_code' in info: # 识别失败
                raise Exception("error_code: %s, error_msg: %s" % (info['error_code'], info['error_msg']))
            print "image:%s" % (filePath)
            for item in info['result']:
                print 'root:%s,keyword:%s' % (item['root'], item['keyword'])
        except Exception, ex:
            print 'BaiduImageClassify.ImageClassify error:%s' % (ex)


if __name__ == '__main__':
    #filePath = '/home/heidai/OnePlus/DCIM/Camera/IMG_20161112_151211.jpg'
    filePath = '/home/heidai/Downloads/20140210170152-1340224008.jpg'
    imageClassify = BaiduImageClassify()
    imageClassify.ImageClassify(filePath)
