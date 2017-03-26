#-*- encoding:utf8 -*-
#-*- author: JH
from selenium import webdriver
import threading
import re
import requests
from lxml import html
import os
from bs4 import BeautifulSoup
import time


info_list = [] #个人信息列表
img_list = [] #首页简介缩略图列表
IMG_links = [] #个人图片链接列表
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2593.0 Safari/537.36',
                   'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                   'cache-control':'max-age=0',
                   'referer':'https://mm.taobao.com/search_tstar_model.htm?',
                   'upgrade-insecure-requests':'1',
                   'accept-encoding':'gzip, deflate, sdch'}


class Mythread (threading.Thread):#从Thread派生出一个子类用于开启多线程
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.args = args
        self.func = func

    def run(self):
        apply(self.func, self.args)


def find_element(html_content):
    root = html.fromstring(html_content)
    tags = root.xpath('//div[@class="girls-list-wrap"]/ul/li')
    print len(tags)
    for t in tags:
        info = (t.xpath('a/@href'), t.xpath('a/div/div[@class="info"]/span/node()'), \
            t.xpath('a/div/div[@class="info row2"]/span[1]/node()'))
        info_list.append(info)
    #print info_list
    #for i in info_list:
        #print i[2][0].encode('utf8')
        #print i[0]
        img_list.append(t.xpath('a/div/div[@class="img"]/img/@*[last()]'))


def get_url():
    try:
        driver = webdriver.PhantomJS(executable_path=r'D:\\phantomjs\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
        driver.get('https://mm.taobao.com/search_tstar_model.htm?')
        htm = driver.page_source
        find_element(htm)
        # print htm
        # root = html.fromstring(htm)
        # tags = root.xpath('//div[@class="girls-list-wrap"]/ul/li')
        # print len(tags)
        # for t in tags:
        #     info = (t.xpath('a/@href'), t.xpath('a/div/div[@class="info"]/span/node()'), \
        #         t.xpath('a/div/div[@class="info row2"]/span[1]/node()'))
        #     info_list.append(info)
        # #print info_list
        # #for i in info_list:
        #     #print i[2][0].encode('utf8')
        #     #print i[0]
        #     img_list.append(t.xpath('a/div/div[@class="img"]/img/@*[last()]'))
        for i in xrange(4):#要得到的页数从第二页开始
            driver.find_element_by_class_name('page-next').click()
            time.sleep(1)
            htm = driver.page_source
            find_element(htm)
            time.sleep(1)
        driver.close()

        #print img_list
    except:
        print '哎呀，再试一次=, ='
    return info_list, img_list


def mkdir(path, num, name_str, address_str):
    isexists = os.path.exists(path)
    if not isexists:
        os.makedirs(path)
        print ('文件夹创建成功')
        with open('E:\\taogirlinfo' + '\\' + name_str+' ' + address_str + '\\' + name_str + '.txt', 'w') as f:
            try:
                f.write(name_str.decode('gbk').encode('utf8') + ':' + info_list[num][2][0].encode('utf8'))
            except:
                print '啊哈，出错了@_@``'
                return False

        f.close()
        return True

    else:
        print name_str.decode('gbk'), ('的文件夹已经存在了')
        return False


def get_mm_img(order):
    global Tags
    IMG_links.append(info_list[order][0][0])
    link = 'http:'+IMG_links.pop()
    try:

        html = requests.get(link, headers=headers)
        cont = html.text
        soup = BeautifulSoup(cont, 'lxml')
        Tags = soup.find_all('img', {"src": re.compile(r".*\.jpg")})

    except:
        print '第' + str(order+1) +'个淘女郎的资料挂啦！！！'


def download_pict(name, address, rank):
    try:
        link = 'http:'+Tags[rank]['src']
        req = requests.get(link, headers=headers)
        img_cont = req.content
        with open('E:\\taogirlinfo'+'\\' + name+' ' + address + '\\' + '/' + str(rank) + '.jpg', 'wb') \
        as picture:
            picture.write(img_cont)
        picture.close()
    except:
        print '第'+str(rank)+'张图挂啦！！！！'


def main():
    get_url()
    loops = []
    for i in xrange(201, len(info_list)):#淘女郎数量
    #for i in range(len(info_list)):
        try:
            name_str = info_list[i][1][0].encode('gbk')
            address_str = info_list[i][1][1].encode('gbk')
            path = r'E:taogirlinfo'+'/'+name_str+' '+address_str
            pic = requests.get('http:'+img_list[i][0]).content
            bool_ = mkdir(path, i, name_str, address_str)
            if bool_:
                with open('E:\\taogirlinfo'+'\\' + name_str+' ' + address_str + '\\' + '/'+'contour' + '.jpg', 'wb') \
                as code:
                    code.write(pic)
                code.close()
                print '正在加载链接...'
                get_mm_img(i)
                print '正在下载第'+str(i+1)+'个淘女郎的资料...'
                if len(Tags) < 40:
                    length = len(Tags)
                else:
                    length = 40
                for r in range(1, length, 2):
                    t = Mythread(download_pict, (name_str, address_str, r))
                    loops.append(t)
                for n in xrange(len(loops)):
                    loops[n].start()
                for n in xrange(len(loops)):
                    loops[n].join()
                loops = []
            else:
                pass
        except:
            print "出错，不要你了@_@``"
            continue
    print '下载完成啦！！！'

if __name__ == '__main__':
    main()





















