import urllib2


class Htmldownloader(object):
    def download(self, url):
        if url is None:
            return None

        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/1.0')
        res = urllib2.urlopen(request)

        if res.getcode() != 200:
            return None

        return res.read()

