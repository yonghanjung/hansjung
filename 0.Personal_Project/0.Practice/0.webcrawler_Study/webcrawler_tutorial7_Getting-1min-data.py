import urllib
import re
import json 

htmltext = urllib.urlopen("http://www.bloomberg.com/markets/chart/data/1D/AAPL:US")
# As not we got the Json Data, We don't need to use Json anymore 

data = json.load(htmltext)
datapoints = data["data_values"]

for point in datapoints:
	print point[1]

print "the number of points is",len(datapoints)
#print datapoints[len(datapoints)-1][1]
