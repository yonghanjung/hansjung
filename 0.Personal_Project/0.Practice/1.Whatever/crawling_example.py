import urllib2
from bs4 import BeautifulSoup

def view_comic_title(page):
    temp = urllib2.urlopen('http://comic.naver.com/webtoon/list.nhn?titleId=20853&weekday=tue&page=%d' % (page))
    html = temp.read().split('<td class="title">')
    for data in html[1:]:
        print data.split('</a>')[0].split(')">')[1]
for i in range(1,10):
    view_comic_title(i)