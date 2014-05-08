from bs4 import BeautifulSoup
import urllib
import mechanize 

mimicopen = open("mimiclist.txt").read()
mimiclist = mimicopen.split("\n")

count = 0


key = "MYOCARDIAL INFARCTION"

for name in mimiclist : 
	try :
		url = "http://www.physionet.org/physiobank/database/mimic2cdb/" + name
		htmlfile = urllib.urlopen(url)
		soup = BeautifulSoup(htmlfile,'lxml')
		htmltext = soup.get_text()
		
		if htmltext.find(key) != -1:
			count = count + 1
			print name 
		 
	except : 
		continue

print count