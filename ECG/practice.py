import re
import urllib
import mechanize 
from threading import Thread

def th(txt1, txt2):
	url = "http://physionet.org/atm/ptbdb/"+ txt1+ "/0/10/export/matlab/"+txt2 + "m.hea"
	htmltext = br.open(url).read()
	if htmltext[0:9] != '<!DOCTYPE':
		response = urllib.urlretrieve (url, newpatientlist2[i]+".txt")
		print response
	else:
		print url

oldpatientfile = open("patientlist.txt")
patientlist = oldpatientfile.read()
newpatientlist = patientlist.split("\n")

oldpatientfile2 = open("patientlist2.txt")
patientlist2 = oldpatientfile2.read()
newpatientlist2 = patientlist2.split("\n")

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


threadlist = []


while i <len(newpatientlist2):
    try:
        t = Thread(target=th, args=(newpatientlist[i], newpatientlist2[i],))
        t.start()
        threadlist.append(t)
        i += 1
    except:
        print "ho"
        i += 1 