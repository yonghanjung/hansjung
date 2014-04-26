from threading import Thread
import urllib
import re

def th(ur):
	url = 'http://www.physionet.org/physiobank/database/mitdb/'+ur+'.hea'
	htmlfile = urllib.urlopen(url)
	htmltext = htmlfile.read()
	maintext = htmltext.split()
	if maintext[0] != '<!DOCTYPE' : print htmltext,'\n'

threadlist = []
ilist = []
jlist = []

for i in range(100,125):
	ilist.append(i)
for j in range(200,235):
	jlist.append(j)

for i in ilist:
	t = Thread(target=th, args=(str(i),))
	t.start()
	threadlist.append(t)

for j in jlist:
	t = Thread(target=th, args=(str(j),))
	t.start()
	threadlist.append(t)

