a = map(int,raw_input().split())
pos = []
neg = []
zo = []

for i in a :
	if i > 0 : pos.append(i)
	elif i == 0 : zo.append(i)
	elif i < 0 : neg.append(i)

print (neg + zo + pos)


