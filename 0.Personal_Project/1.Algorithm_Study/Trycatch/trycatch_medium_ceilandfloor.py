a = input()
b = map(int,raw_input().split())
b.sort()
print b
mini = 10000
maxi = 10000
for i in b:
	if a <= i and abs(i - a) < mini :
		mini = abs(i-a)
		cand1 = i
	if a >= i and abs(i-a) < maxi :
		maxi = abs( i-a)
		cand2 = i

print cand1
print cand2
