import urllib #Library for Internet 

urls = ["http://google.com","http://nytimes.com", "http://CNN.com"]

i = 0

while i<len(urls) :
	htmlfile = urllib.urlopen(urls[i])
	htmltext = htmlfile.read()
	print htmltext
	i += 1

