import urllib
import re

stockfile = open("stocklist.txt")
NASlist = stockfile.read()
newNASlist = NASlist.split("\n")

i = 0
while i < len(newNASlist):
	url = "https://www.google.com/finance/getprices?q="+newNASlist[i]+"&x=NASD&i=120&p=25m&f=c&df=cpct&auto1"
	htmltext = urllib.urlopen(url).read()
	print "The price of",newNASlist[i],"is",htmltext.split()[len(htmltext.split())-1]
	i += 1
