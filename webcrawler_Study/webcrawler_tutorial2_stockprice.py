import urllib
import re

htmlfile = urllib.urlopen("http://finance.yahoo.com/q?s=AAPL&ql=1")
htmltext = htmlfile.read()

regex = '<span id="yfs_l84_aapl">(.+?)</span>'
pattern = re.compile(regex)

price = re.findall(pattern,htmltext)

print price
