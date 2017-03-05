#!/usr/bin/env python3

import os
import re
import urllib.request
import urllib.parse
import urllib.error

class meizitu:
    def __init__(self):
        self.url = 'http://www.meizitu.com/'
        self.headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.27 Safari/537.36",
            }
        self.pattern = re.compile('<div.*?postContent(.*?)</p>',re.S)
        self.pict = re.compile('.*?src="(.*?)"',re.S)
        self.savepath = '/home/khe/Pictures/meizitu/'

    def getPage(self, idx):
        pageurl = self.url + 'a/' + str(idx) + '.html'
        try:
            request = urllib.request.Request(
                    url = pageurl,
                    headers = self.headers)
            response = urllib.request.urlopen(request)
            page = response.read().decode('gbk')
            self.getPict(page, idx)
        except urllib.error.URLError as e:
            print (e)
            
    def getPict(self, page, idx):
        content = re.findall(self.pattern, page)
        if content:
            picts = re.findall(self.pict, content[0])
            if picts:
                self.mkdir(self.savepath+str(idx))
                for i, pict in enumerate(picts):
#                    name = self.savepath+str(idx)+'/'+str(i+1)+'.jpg'
#                    self.saveImg(pict, name)
                    self.saveImg_wget(pict, self.savepath+str(idx))
        else:
            return False

    def saveImg(self, imgUrl, filename):
        try:
            request = urllib.request.Request(
                    url = imgUrl,
                    headers = self.headers)
            u = urllib.request.urlopen(request)
            data = u.read()
            f = open(filename, 'wb')
            f.write(data)
            f.close()
            print ("Saved :{0}".format(filename))
            return True
        except urllib.error.URLError as e:
            print (e)
            return False

    def saveImg_wget(self, imgUrl, path):
        os.system('wget {0} -P {1}'.format(imgUrl, path))
            

    def mkdir(self, path):
        if os.path.exists(path):
            return
        os.makedirs(path)
        print ("Creating New Dir:", path)


mzt = meizitu()
for i in range(120, 789):
    mzt.getPage(i)
