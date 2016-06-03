


class UrlManager(object):
    def __init__(self):
        self.page_urls = set()
        self.img_urls = set()

    def add_page_url(self, url):
        if url is None:
            return
        self.page_urls.add(url)

    def add_page_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_page_url(url)

    '''def add_img_url(self, lnk):
        if lnk is None:
            return
        self.img_urls.add(lnk)

    def add_img_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_img_url(url)'''

    def has_page_url(self):
        return len(self.page_urls) != 0

    def get_page_url(self):
        new_url = self.page_urls.pop()
        return new_url