import urllib
import re

symbolfile = open("stocklist.txt")
symbolslist = symbolfile.read()
uppernewsymbolslist = symbolslist.split("\n")
newsymbolslist = [x.lower() for x in uppernewsymbolslist]
i = 0

while i <len(symbolslist):
	url = "http://finance.yahoo.com/q?s="+newsymbolslist[i] +"&ql=1"
	htmlfile = urllib.urlopen(url)
	htmltext = htmlfile.read()
	regex = '<span id="yfs_l84_'+newsymbolslist[i] +'">(.+?)</span>'
	pattern = re.compile(regex)
	price = re.findall(pattern,htmltext)
	print "the price of",uppernewsymbolslist[i],"is", price
	i += 1
