import re
import urllib
import mechanize 
from threading import Thread

oldpatientfile = open("patientlist.txt")
patientlist = oldpatientfile.read()
newpatientlist = patientlist.split("\n")

oldpatientfile2 = open("patientlist2.txt")
patientlist2 = oldpatientfile2.read()
newpatientlist2 = patientlist2.split("\n")

oldpatientfile3 = open("patientlist3.txt")
patientlist3 = oldpatientfile3.read()
newpatientlist3 = patientlist3.split("\n")

i = 0

br = mechanize.Browser(factory=mechanize.RobustFactory()) # Use this because of bad html tags in the html...

br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'),
                 ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                 ('Accept-Encoding', 'gzip,deflate,sdch'),                  
                 ('Accept-Language', 'en-US,en;q=0.8'),                     
                 ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]

print "ho"

## MAT FILE 
while i < len(newpatientlist2) :
	try:
		url = "http://physionet.org/atm/ptbdb/"+ newpatientlist[i] + "/0/10/export/matlab/"+newpatientlist2[i] + "m.mat"
		htmltext = br.open(url).read()
		if htmltext[0:9] != '<!DOCTYPE':
			response = urllib.urlretrieve (url, newpatientlist3[i]+"_"+ newpatientlist2[i] +".mat")
			print response
			i += 1
		else:
			print url
			i += 1
	except:
		i += 1

i = 0
## HEA FILE 
while i < len(newpatientlist2) :
	try:
		url = "http://physionet.org/atm/ptbdb/"+ newpatientlist[i] + "/0/10/export/matlab/"+newpatientlist2[i] + "m.hea"
		htmltext = br.open(url).read()
		if htmltext[0:9] != '<!DOCTYPE':
			response = urllib.urlretrieve (url, newpatientlist3[i]+"_"+ newpatientlist2[i] + "_header_" +  ".txt")
			print response
			i += 1
		else:
			print url
			i += 1
	except:
		i += 1

i = 0
## Info FILE 
while i < len(newpatientlist2) :
	try:
		url = "http://physionet.org/atm/ptbdb/"+ newpatientlist[i] + "/0/10/export/matlab/"+newpatientlist2[i] + "m.info"
		htmltext = br.open(url).read()
		if htmltext[0:9] != '<!DOCTYPE':
			response = urllib.urlretrieve (url, newpatientlist3[i]+"_"+ newpatientlist2[i] + "_info_" + ".txt")
			print response
			i += 1
		else:
			print url
			i += 1
	except:
		i += 1
