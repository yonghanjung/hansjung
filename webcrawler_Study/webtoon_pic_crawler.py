import mechanize
from bs4 import BeautifulSoup
import urllib
import unicodedata

def soupsoup(url):
	html = urllib.urlopen(url)
	soup = BeautifulSoup(html)
	return soup

def main():
	br = mechanize.Browser(factory=mechanize.RobustFactory()) # Use this because of bad html tags in the html...

	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)

	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

	br.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'),
	('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
	('Accept-Encoding', 'gzip,deflate,sdch'),                  
	('Accept-Language', 'en-US,en;q=0.8'),                     
	('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]

	url = "type your url"
	soup = soupsoup(url)
	box = []
	for link in soup.find_all('img'):
		a = link.get('src')
		a = unicodedata.normalize('NFKD', a).encode('ascii','ignore')
		box.append(a)
	print box
	for i in range(len(box)):
		print box[i]
		word = "uf.daum.net/image"
		a = word in box[i]
		print a 
		if word in box[i] :
			urllib.urlretrieve(box[i],str(i)+".jpg")

if __name__ == "__main__" :
	main()