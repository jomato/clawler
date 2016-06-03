from bs4 import BeautifulSoup
import re


class parser(object):
    def _get_img_urls(self, page_url, soup):
        i_urls = set()

        links = soup.find_all('img')
        for link in links:
            new_url = link['src']
            i_urls.add(new_url)
        return i_urls

    def _get_page_urls(self,page_url,soup):
        p_urls = set()

        lnks = soup.find_all('a', href=re.compile(r'http://jandan.net/ooxx/page-(.)+#comments'))
        for lnk in lnks:
            new_lnk = lnk['href']
            p_urls.add(new_lnk)
        return p_urls

    def parse(self, page_url, html_cont):

        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        img_urls = self._get_img_urls(page_url, soup)
        page_urls = self._get_page_urls(page_url, soup)
        return img_urls, page_urls