from bs4 import BeautifulSoup
import urllib

html = urllib.urlopen('http://comic.naver.com/webtoon/weekday.nhn')
soup = BeautifulSoup(html,"lxml")
titles = soup.find_all('a','title')

for title in titles:
	print 'title:{0:1s} link:{1:1s}\n'.format(title['title'].encode('utf-8'), title['href'].encode('utf-8'))

