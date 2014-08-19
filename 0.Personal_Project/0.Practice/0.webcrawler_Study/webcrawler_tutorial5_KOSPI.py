import urllib
import re

stockfile = open("Kospi.txt")
KOSlist = stockfile.read()
newKOSlist = KOSlist.split("\n")

kospiname = open("Kospiname.txt")
kospinamelist = kospiname.read()
newkospinamelist = kospinamelist.split("\n")

i = 0
while i < len(newKOSlist):
	url = 'http://stock.daum.net/item/ajax/checkprice.daum?code='+newKOSlist[i]	
	htmltext = urllib.urlopen(url).read()
	regex = "price: {price: '(.+?)', updown"
	pattern = re.compile(regex)
	price = re.findall(pattern,htmltext)
	print newkospinamelist[i],":",price 
	i += 1
