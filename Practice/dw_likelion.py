import urllib2
from bs4 import BeautifulSoup

headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
	"Accept-Encoding": "gzip,deflate,sdch"
	"Accept-Language": "en-US,en;q=0.8,ja;q=0.6"
	"Cache-Control": "max-age=0"
	"Connection": "keep-alive"
	"Cookie": "sessionid=41c4b54595d7d91877139d134f5b2a96; arara_checksum=d40e363aafae39dfd06253e13c4a99046eb377cf; __utma=245894612.1078171952.1406543832.1406543832.1406543832.1; __utmb=245894612.1.10.1406543832; __utmc=245894612; __utmz=245894612.1406543832.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
	"Host": "ara.kaist.ac.kr"
	"If-Modified-Since": "Mon, 28 Jul 2014 10:37:22 GMT"
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36 "
}

request = urllib2.Request(url_needed_login , headers = headers)
contents = urllib.urlopen(request).read()

soup = BeautifulSoup(contents)
print soup.title
