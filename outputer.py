# -*-  coding:utf-8 -*-
import urllib2

class Outputer(object):
    def __init__(self):
        self.Data = []

    def add_img_url(self, lnk):
        if lnk is None:
            return
        self.Data.append(lnk)


    def collect_data(self, data):
        if data is None:
            return
        for d in data:
            self.add_img_url(d)

    def output_html(self):
        for D in self.Data:
            req = urllib2.Request(D)
            req.add_header('User-Agent', 'Mozilla/2.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
            cont = urllib2.urlopen(req).read()
            with open(u'E:\Pict'+'/'+D[-11:],'wb') as code:
                code.write(cont)