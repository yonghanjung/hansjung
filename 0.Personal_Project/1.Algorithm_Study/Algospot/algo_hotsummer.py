howmany = input()
judge = []

for trial in range(0,howmany):
	sum = 0
	usage = []
	## Initialize 

	goal = input()
	usage = map(int,raw_input().split())
	for com in range(0,len(usage)):
		sum += usage[com]
	if sum <= goal:
		judge.append("YES")
	else:
		judge.append("NO")


for i in range(0,howmany):
	print judge[i]