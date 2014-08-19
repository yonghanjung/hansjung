import urllib
import re
import json

NASfile = open("stocklist.txt")
NASread = NASfile.read()
NASlist = NASread.split("\n")

i = 0
while i < len(NASlist):
	url = "http://www.bloomberg.com/markets/watchlist/recent-ticker/"+NASlist[i]+":US"
	htmltext = urllib.urlopen(url)

	data = json.load(htmltext) #it takes only a file, it must occur an error!  
# It is file distinguished by a Hash Map, which will work as a key
	
	print data["disp_name"],":", data["last_price"] #works like an array, but it works with a key, not an index.
	i+= 1
