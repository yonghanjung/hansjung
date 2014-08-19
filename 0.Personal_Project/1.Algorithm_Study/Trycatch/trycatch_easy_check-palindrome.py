a = input()
digit = len(str(a))
str1 = [] 
for i in range(0,digit):
	str1.append(a%10)
	a /= 10

str2 = str1.reverse()

if (str1 == str2):
	 print "TRUE" 
else:
	 print "FALSE" 

 
