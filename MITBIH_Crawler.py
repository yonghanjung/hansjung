import urllib
import re

for i in range(100,125):
	url = 'http://www.physionet.org/physiobank/database/mitdb/'+str(i)+'.hea'
	htmlfile = urllib.urlopen(url)
	htmltext = htmlfile.read()
	maintext = htmltext.split()
	if maintext[0] == '<!DOCTYPE' : continue
	print htmltext,'\n'

for j in range(200,235):
	url = 'http://www.physionet.org/physiobank/database/mitdb/'+str(i)+'.hea'
	htmlfile = urllib.urlopen(url)
	htmltext = htmlfile.read()
	maintext = htmltext.split()
	if maintext[0] == '<!DOCTYPE' : continue
	print htmltext,'\n'
