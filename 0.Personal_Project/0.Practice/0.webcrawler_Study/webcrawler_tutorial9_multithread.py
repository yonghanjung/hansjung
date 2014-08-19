from threading import Thread
import urllib 
import re

def th(ur):
	regex = "<title>(.+?)</title>"
	pattern = re.compile(regex)
	# visit and open 
	htmltext = urllib.urlopen(ur).read()
	results = re.findall(pattern,htmltext)
	print results
#define the task you want to through multithread 

urls = "http://google.com http://cnn.com http://yahoo.com http://wikipedia.com".split()
threadlist = []

for u in urls:
	t = Thread(target = th,args=(u,))
	t.start()
	threadlist.append(t) # datastructure storing thread 

for b in threadlist:
	b.join()
