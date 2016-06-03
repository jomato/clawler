# -*-  coding:utf-8 -*-
import downloader
import urls_manager
import outputer
import go_parser


class SpiderMain(object):
    def __init__(self):
        self.urls = urls_manager.UrlManager()
        self.downloader = downloader.Htmldownloader()
        self.Parser = go_parser.parser()
        self.outputer = outputer.Outputer()


    def crawl(self, root_url):
        self.urls.add_page_url(root_url)
        while self.urls.has_page_url():
            try:

                new_url = self.urls.get_page_url()
                html_cont = self.downloader.download(new_url)
                img_urls, page_urls = self.Parser.parse(new_url, html_cont)
                #for i in img_urls:
                    #print i
                #for p in page_urls:
                    #print p
                self.urls.add_page_urls(page_urls)
                self.outputer.collect_data(img_urls)

            except:
                 '无法获取'

        self.outputer.output_html()
        #D = self.outputer.Data
        #for d in D:
            #print d


if __name__ == '__main__':
    root_url = 'http://jandan.net/ooxx/page-1970#comments'
    SM = SpiderMain()
    SM.crawl(root_url)
