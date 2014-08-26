# -*- coding: utf-8 -*-
__author__ = 'jeong-yonghan'

import urllib

data = []
for idx in range(100,235):
    data.append(idx)

for mydata in data:
    url = "http://physionet.org/atm/mitdb/" + str(103) + "/atr/0/e/rr/T/rr.txt"
    htmltext = urllib.urlopen(url).read()
    if htmltext[0] == '<':
        print "oops",mydata
    else:
        print mydata

