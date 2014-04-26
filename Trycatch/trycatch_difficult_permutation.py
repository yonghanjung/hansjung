import itertools

a = raw_input()
b = list(itertools.permutations(a,len(a)))
s = ''
c = []
for i in range (0,len(b)):
	c.append(s.join(b[i]))

c = list(set(c))
for i in range(0,len(c)):
	print c[i],
