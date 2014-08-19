import itertools 
a = map(str,raw_input().split())
s = ' '
print "the number of subsets are %d"%(2 ** len(a))
for i in range(1,len(a)+1):
	b = list(itertools.combinations(a,i))
	for j in range(0,len(b)):
		print s.join(b[j])



