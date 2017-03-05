#!/usr/bin/env python3

import urllib.request
import urllib.parse
from http.cookiejar import CookieJar
import re
import os

class MTeam:
    def __init__(self):
        self.url = 'https://tp.m-team.cc/'
        self.loginUrl= 'https://tp.m-team.cc/takelogin.php'
        self.cookies = CookieJar()
        self.postdata = urllib.parse.urlencode({
            'username': '',
            'password': ''
        }).encode('utf-8')
        self.headers ={
            'origin': "https://tp.m-team.cc",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.8",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.27 Safari/537.36",
            'content-type': "application/x-www-form-urlencoded",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'cache-control': "no-cache",
            'referer': "https://tp.m-team.cc/login.php",
            'connection': "keep-alive"
        } 
        self.pattern = re.compile('<td.*?torrentimg">.*?title="(.*?)" href="(.*?)">',re.S) 
        self.cover = re.compile('<div.*?kdescr.*?src="(.*?)"', re.S)
        self.pict = re.compile('Previewurl\(\'(.*?)\'\)', re.S)
        self.name = re.compile('artist.*?<b>(.*?)</b>', re.S)
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
        self.coverdict = {}
        self.pictdict = {}
        self.savepath = "/home/khe/Pictures/artists/"
    
    def login(self):
        request = urllib.request.Request(
                url = self.loginUrl,
                data = self.postdata,
                headers = self.headers)
        result = self.opener.open(request)

    def getHDcensoredPage(self, page):
        self.HDcensoredUrl = 'https://tp.m-team.cc/adult.php?inclbookmarked=0&incldead=1&spstate=0&cat=410&page=' + str(page)
        try:
            result = self.opener.open(self.HDcensoredUrl) 
        except:
            return
        content = result.read().decode('utf-8')
        items = re.findall(self.pattern, content)
        for item in items:
            self.getTorrentPage(item[1])

    def getTorrentPage(self, idx):
        torrentPage = self.url + idx
        try:
            result = self.opener.open(torrentPage)
        except:
            return
        content = result.read().decode('utf-8')
        name = re.search(self.name, content)
        if name:
            name = name.group(1).strip()
        else:
            return

        if name in self.coverdict:
            self.coverdict[name] += 1
        else:
            self.coverdict[name] = 1
            self.pictdict[name] = 0
            self.mkdir(self.savepath+name)
        coverSave = self.savepath+name+"/cover/"+str(self.coverdict[name])+".jpg"
        picts = re.findall(self.pict, content)
        if picts:
            if self.saveImg(picts[0], coverSave):
                print("Saving: ", coverSave)
            else:
                self.coverdict[name] -= 1
            picts.pop(0)
    
        for pict in picts:
            self.pictdict[name] += 1
            pictSave = self.savepath+name+"/"+str(self.pictdict[name])+".jpg"
            if self.saveImg(pict, pictSave):
                print("Saving: ", pictSave)
            else:
                self.pictdict[name] -= 1


    def printDict(self):
        for key, value in self.coverdict.items():
            print (key)
            print ("cover:", value)
            print ("pict:", self.pictdict[key])

    def saveImg(self, imgUrl, filename):
        if not imgUrl.startswith('http'):
            imgUrl = self.url+imgUrl
        try:
            u = urllib.request.urlopen(imgUrl)
            data = u.read()
            f = open(filename, 'wb')
            f.write(data)
            f.close()
            return True
        except:
            return False

    def mkdir(self, path):
        if os.path.exists(path):
            return
        os.makedirs(path)
        print ("Creating New Dir:", path)
        coverpath = path + "/cover"
        os.makedirs(coverpath)

mt = MTeam()
mt.login()
for i in range(96):
    mt.getHDcensoredPage(i)
    print ("Page {0} finished!".format(i))
