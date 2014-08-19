# -*- coding: cp949 -*-

# http://blog.naver.com/kirokkk123
# ÀÍ·æÀÌ¾ß

import urllib
from bs4 import BeautifulSoup
import re

page = urllib.urlopen('http://comic.naver.com/webtoon/weekday.nhn')
soup = BeautifulSoup(page,'lxml')
webtoons = soup.find_all("a", "title")

webtoon_title=[]
webtoon_number=[]
for webtoon in webtoons:
    webtoon_title.append(webtoon['title'])
    webtoon_number.append(re.search('\d+',webtoon['href']).group())

n=len(webtoon_number)

webtoon_relatives=[]
i=0
while i<n:
    page = urllib.urlopen('http://comic.naver.com/webtoon/detail.nhn?titleId='+webtoon_number[i]+'&no=1')
    soup = BeautifulSoup(page,'lxml')
    relatives = soup.find_all("div",attrs={'class':'thumb6'})
    relative_list=[]
    for relative in relatives:
        relative_list.append(relative.a['title'])
        now=re.search('\d+',relative.a['href']).group()
        if(not now in webtoon_number):
            webtoon_number.append(now)
            webtoon_title.append(relative.img['title'])            
    webtoon_relatives.append(relative_list)
    i=i+1
    n=len(webtoon_number)

f=open('webtoon_title.txt','w')
for i in range(n):
    f.write(webtoon_title[i].encode('utf-8'))
    f.write('\n')
f.close()

f=open('webtoon_relatives.txt','w')
for i in range(n):
    for j in range(len(webtoon_relatives[i])):
        f.write(webtoon_relatives[i][j].encode('utf-8'))
        f.write('\t')
    f.write('\n')
f.close()

##print webtoon_relatives[0].encode('utf-8')multithread 순서대로 출력
