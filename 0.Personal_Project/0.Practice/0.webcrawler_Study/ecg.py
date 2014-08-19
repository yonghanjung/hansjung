import re
import urllib

urls = 'http://physionet.org/cgi-bin/atm/ATM'
htmlfile = urllib.urlopen(urls)
htmltext = htmlfile.read()

regex = '<option value(.+?)re</option>'
pattern = re.compile(regex)

address = re.findall(pattern,htmltext)
print address
