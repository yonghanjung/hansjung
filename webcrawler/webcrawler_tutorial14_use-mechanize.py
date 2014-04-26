import urllib
from bs4 import BeautifulSoup
import urlparse
import mechanize
# Simulate the browser

url  = "http://sparkbrowser.com"
count = 0

# The smartest method ==> No hashtop such tha sparkbrowser.com#top 

br = mechanize.Browser()
#Just copy how the Browser acts 
br.open(url)
for link in br.links():
	newurl = urlparse.urljoin(link.base_url,link.url)
	b1 = urlparse.urlparse(newurl).path
	b2 = urlparse.urlparse(newurl).hostname
	print "http://"+b2+b1
	count += 1
print count
		# IN this way, we don't include Javascript such as #top 
		# Best way



# Method_3. NOT WORK Use urlparse.urlparse(tag['href']).path or hostname
'''
htmlfile = urllib.urlopen(url)
soup = BeautifulSoup(htmlfile)

for tag in soup.find_all('a',href=True):
	b1 = urlparse.urlparse(tag['href']).hostname
	b2 = urlparse.urlparse(tag['href']).path
	print "http://"+str(b1)+str(b2)
'''

# Method_1. Use BeautifulSoup 
'''
htmlfile = urllib.urlopen(url)
soup = BeautifulSoup(htmlfile)

for tag in soup.find_all('a',href=True):
	print tag['href']
'''


# Method_2. Use mechanize 
'''
br = mechanize.Browser()
br.open(url)

for link in br.links():
	newurl = urlparse.urljoin(link.base_url,link.url)
	print newurl
	count += 1
print count
'''
