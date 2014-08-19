import mechanize
import urllib
from bs4 import BeautifulSoup
import unicodedata
import csv


def parserparser(url):
    htmlread = mechanize.urlopen(url)
    htmltext = htmlread.read()
    soupsoup = BeautifulSoup(htmltext)
    return soupsoup


def main():
    url = "http://elibrary-data.imf.org/DataReport.aspx?c=7183654&d=33060&e=141512"
    soup = parserparser(url)

    table = soup.find_all('tr', {"class": "row_3"})
    '''
    Current_Account_Balance = 5
    Capital_Account_Balance = 6
    Financial_Account_Balance = 7
    Net_Errors_and_Omissions = 8
    NET_IIP = 10
    TOTAL_IIP_Asset = 11
    TOTAL_IIP_Liab = 12
    '''

    needed = [3, 5, 6, 7, 8, 10, 11, 12]
    csv_format = []

    for needs in needed:
        try:
            temp = table[needs].get_text()
        except:
            print needs, type(needs)
        temp = unicodedata.normalize('NFKD', temp).encode('ascii','ignore')
        temp = temp.split('\n')
        temp = [x for x in temp if x != ' ']
        temp = [x for x in temp if x != '']
        temp = [x for x in temp if x != '...']
        if needs == 3:
            temp.insert(0,'year')
        csv_format.append(temp)

    myfile = open('test.csv','wb')
    wr = csv.writer(myfile,quoting=csv.QUOTE_ALL)
    for x in csv_format:
        wr.writerow(x)

if __name__ == "__main__":
    main()
