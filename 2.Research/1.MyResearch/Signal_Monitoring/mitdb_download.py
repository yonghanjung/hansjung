__author__ = 'jeong-yonghan'

from bs4 import BeautifulSoup
import urllib2
import mechanize

datanum = []
for i in range(100,235):
    datanum.append(i)

print datanum

for num in datanum:
    url = "http://physionet.org/atm/mitdb/" + str(num) + "/atr/0/e/rr/T/rr.txt"
    try:
        urllib2.urlopen(url)
        urllib2.urlretrieve(url,str(num)+".txt")
    except:
        print num
        continue


