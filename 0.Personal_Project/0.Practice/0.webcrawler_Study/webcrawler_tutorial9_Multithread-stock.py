from threading import Thread
import urllib
import re

def th(ur):
	base = "http://finance.yahoo.com/q?s="+ur
	regex = '<span id="yfs_l84_'+ur.lower()+'">(.+?)</span>'
	pattern = re.compile(regex)
	htmltext = urllib.urlopen(base).read()
	results = re.findall(pattern,htmltext)
	print "the price of",str(ur),"is",str(results[0])

stocklist = open("stocklist.txt").read()
stocklist = stocklist.split("\n")
print stocklist

threadlist = []

for u in stocklist:
	t = Thread(target=th, args=(u,))
	t.start()
	threadlist.append(t)

for b in threadlist:
	b.join()
