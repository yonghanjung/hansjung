# Another elements of url not with / this form 
import urllib
from bs4 import BeautifulSoup
import urlparse 

url = "http://nytimes.com"
htmltext = urllib.urlopen(url)
soup = BeautifulSoup(htmltext)

for tag in soup.find_all('a',href = True):
	raw = tag['href']
	b1 = urlparse.urlparse(tag['href']).hostname
	b2 = urlparse.urlparse(tag['href']).path # * 
	print str(b1) + str(b2)

#* Spider trap:
	# We don't use the method used in last tutorial
	# because sometimes WEB gives certain ID to users and Spider web might be confused it as all different website
	# That is why it is good to use urlparse.path


