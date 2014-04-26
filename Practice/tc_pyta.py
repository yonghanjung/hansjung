from itertools import combinations
sol = []
inp = map(int,raw_input().split())

A = list(combinations(inp,3))

for i in range(0,len(A)):
	add = 0
	if pow(A[i][0],2) + pow(A[i][1],2) is pow(A[i][2],2):
		sol.append(A[i])

for i in range(0,len(sol)):
	print sol[i]