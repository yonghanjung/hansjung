import mechanize

oldpatientfile = open("patientlist.txt")
patientlist = oldpatientfile.read()
newpatientlist = patientlist.split("\n")

oldpatientfile2 = open("patientlist2.txt")
patientlist2 = oldpatientfile2.read()
newpatientlist2 = patientlist2.split("\n")

oldpatientfile3 = open("patientlist3.txt")
patientlist3 = oldpatientfile3.read()
newpatientlist3 = patientlist3.split("\n")

# Open filelist 

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

## Say that I am not a Robot 

## Save to the text file 
f = file('determine.txt','a+')
f.truncate() # File Initialize

i = 0
key1 = 'Myocardial infarction'
key2 = 'Healthy control'

while i < len(newpatientlist2):
	try:
		url = "http://physionet.org/atm/ptbdb/"+ newpatientlist[i] + "/0/10/export/matlab/"+newpatientlist2[i] + "m.hea"
		htmltext = br.open(url).read()
		Jiyeon1 = htmltext.find(key1)
		Jiyeon2 = htmltext.find(key2)
		f.write(str(i+1))
		if Jiyeon1 != -1 :
			f.write(' ' + key1 + ' ' + str(1) + '\n')
		elif Jiyeon2 != -1 :
			f.write(' ' + key2 + ' ' + str(0) + '\n')
		else :
			f.write(' ' + 'others' + ' ' + str(2) + '\n')
		i += 1
	except:
		i = i+1

f.close()