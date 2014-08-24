# -*- coding: utf-8 -*-
__author__ = 'jeong-yonghan'


__author__ = 'jeong-yonghan'

from bs4 import BeautifulSoup
import mechanize
import urllib

def main():
    import unicodedata
    def download_html(url):
        htmlread = mechanize.urlopen(url)
        htmltext = htmlread.read()
        soupsoup = BeautifulSoup(htmltext)
        return soupsoup
    url = "http://www.likelion.net"
    soup = download_html(url)
    img_list = []; name_list = []
    for img in soup.find_all('img',{'class' : 'scaleimg'}):
        a = img.get('src')
        a = unicodedata.normalize('NFKD', a).encode('ascii','ignore')
        img_list.append(a)
        print a

    name_list.append('이두희 대장님')
    name_list.append('최용철 대장님')
    for name in soup.find_all('p',{'class' : 'project-title'}):
        strname = str(name)
        strname = strname[25:]
        strname = strname[:-4]
        name_list.append(strname)
        print strname


    # Download
    for idx in range(len(img_list)):
        urllib.urlretrieve(url + "/" + img_list[idx], name_list[idx]+".jpg")




if __name__ == "__main__":
    main()