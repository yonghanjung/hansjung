import urllib 
import json

#Open up the stocklist.txt
NASfile = open("stocklist.txt")
NASload = NASfile.read()
NASlist = NASload.split("\n")

for symbol in NASlist:
	myfile = open("/home/hansjung/Python/stockprogram/"+symbol+".txt","w+")
	myfile.close()
	
	htmltext = urllib.urlopen("http://www.bloomberg.com/markets/chart/data/1D/"+symbol+":US")
	data = json.load(htmltext) #When we use Json, we don't use .read()
	datapoints = data["data_values"]

	myfile = open("/home/hansjung/Python/stockprogram/"+symbol+".txt","a")	

	for point in datapoints:
		myfile.write(str(symbol+","+str(point[0])+","+str(point[1])))
	myfile.close()
