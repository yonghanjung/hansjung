import urllib
from bs4 import BeautifulSoup
import unicodedata

def tran(a):
	return unicodedata.normalize('NFKD', a).encode('ascii','ignore')

def main():
	url = "http://www.cs.cmu.edu/~guestrin/Class/10701/schedule.html"
	html = urllib.urlopen(url)
	soup = BeautifulSoup(html)

	namebox = []
	for link in soup.find_all("a"):
		namebox.append(link.get('href'))
	
	downindex = 0;

	for boxelement in range(len(namebox)):
		#try:
			if "slides" in namebox[boxelement] :
				urllib.urlretrieve(namebox[boxelement], str(downindex) + ".pdf")
				downindex += 1
		# except:
			# boxelement +=1 
if __name__ == "__main__":
	main()