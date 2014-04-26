import urllib
import re

kospifile = open("Kospi.txt")
kospilist = kospifile.read()
newkospilist = kospilist.split("\n")

kospiname = open("Kospiname.txt")
kospinamelist = kospiname.read()
newkospinamelist = kospinamelist.split("\n")

i = 0
while i < len(newkospilist):
	url = "http://stock.daum.net/item/main.daum?code="+newkospilist[i]
	htmlfile = urllib.urlopen(url)
	htmltext = htmlfile.read()
	regex = '<em class="curPrice up">(.+?)</em>' 	
	pattern = re.compile(regex)
	price = re.findall(pattern,htmltext)
	if  price == []:
		regex = '<em class="curPrice down">(.+?)</em>' 	
		pattern = re.compile(regex)
		price = re.findall(pattern,htmltext)
		if price == []:
			regex = '<em class="curPrice keep">(.+?)</em>' 	
			pattern = re.compile(regex)
			price = re.findall(pattern,htmltext)

	print "the price of",newkospinamelist[i],"is",price[0]
	i += 1
