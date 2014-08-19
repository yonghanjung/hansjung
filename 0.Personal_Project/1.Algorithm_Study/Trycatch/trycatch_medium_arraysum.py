import itertools

a = map(int,raw_input().split())
ans = []
for i in range(0,len(a)):
	add = 0
	for j in range(i,len(a)):
		add += a[j]
		ans.append(add)

print max(ans)	
