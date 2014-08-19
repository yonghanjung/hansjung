a = map(int,raw_input().split())
b = map(int,raw_input().split())
s = ' '
c = list(set(a).intersection(set(b)))
for i in range (0,len(c)):
	print c[i],
