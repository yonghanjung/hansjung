# Introduction
# : Page spider 
# Building Spider Algorithm 
# Que and stack of algorithm
# Only way to spider algorithm is stack or quee 
# To explore more pages and visit new pages and remember which pages are already visited 
# URLparse --> Allows us to explore more and more pages
 
import urlparse
import urllib
from bs4 import BeautifulSoup 
# BS is a library  

url = "http://www.adbnews/area51"
# what URL we are going to visit 

urls = [url] #stack of urls to scrape 
visited = [url] #Historic record of urls 
#stack : sort of array that we put every canditates that we want to push to visit if it is not in historical boxex collecting already visited by us
#Two stacks  

while len(urls) > 0:
# Reason to use while roop is urls is a list will grow and contract to zero.
# grow to the max and will shirink. No more needs to have more urls try:
	try :	
		htmltext = urllib.urlopen(urls[0])
		# it is a queue. Because the queue is FIFO. 
		# Because the Queue adds to the end and removes from end of the list. 
		# Queue : FIFO
		# Stack : LIFO 
	except : 
		print urls[0]
		# Because most of errors are occured from trying to visit sites actually not there 
	
	soup = BeautifulSoup(htmltext)
	# Convert htmltext to BS objects (document FILE) 
 	
	urls.pop(0)
	print len(urls)
	# If urls contains several elements, we can deleted the first one by method of stack 

	for tag in soup.findAll('a',href = True):
		b1 = urlparse.urlparse(tag['href']).hostname
		b2 = urlparse.urlparse(tag['href']).path
		web = "http://"+str(b1)+str(b2)
		# This is the way how to use a stack box 
		# This is the way to use BS to find the link 
		if web not in visited:
			urls.append(web)
			visited.append(web)
	# Type of tag is a object of class BS, and tag['href'] is 'str'

print visited
	 
		 
