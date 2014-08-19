from bs4 import BeautifulSoup

htmltext = open("htmldoc.html")
soup = BeautifulSoup(htmltext)
print soup.title

