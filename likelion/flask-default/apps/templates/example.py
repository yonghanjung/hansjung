import urllib2
from bs4 import BeautifulSoup


class scrolled_data(object):

    def __init__(self, url):
        self.url = url
        self.source = urllib2.urlopen(self.url).read()\
            .decode('utf-8', 'ignore')
        self.soup = BeautifulSoup(self.source)

dcurl = "http://gall.dcinside.com/board/lists/?id=tree&page=3"
data = scrolled_data(dcurl)

context = data.soup.findAll('td', attrs={'class': 't_subject'})

for each in context:
    if each.a.string:
        print each.a.string
